#include "rclcpp_action/rclcpp_action.hpp"
#include "plansys2_msgs/msg/action_execution_info.hpp"
#include "plansys2_msgs/msg/plan.hpp"
#include "plansys2_pddl_parser/Utils.h"

#include "bt_plansys_turtlebot/task_controller_node.hpp"

TaskControllerNode::TaskControllerNode(): rclcpp::Node("navigate_node"){}

bool TaskControllerNode::init(){
    domain_expert_ = std::make_shared<plansys2::DomainExpertClient>();
    problem_expert_ = std::make_shared<plansys2::ProblemExpertClient>();
    planner_client_ = std::make_shared<plansys2::PlannerClient>();
    executor_client_ = std::make_shared<plansys2::ExecutorClient>();

    // get predicates, instances and goal
    this->init_knowledge();

    // get domain, problem and plan
    auto domain = domain_expert_->getDomain();
    auto problem = problem_expert_->getProblem();
    auto plan = planner_client_->getPlan(domain, problem);

    if(!plan.has_value()){
        std::cout << "Could not find a plan to reach goal "
                  << parser::pddl::toString(problem_expert_->getGoal())
                  << std::endl;

        return false;
    }

    // print the plan to console
    std::cout << "---------------- Plan ----------------" << std::endl;
    for(const auto &plan_item: plan.value().items){
        std::cout << plan_item.time << ":\t" << plan_item.action << "\t[" <<
            plan_item.duration << "]" << std::endl;
    }
    std::cout << "--------------------------------------" << std::endl;

    if(!executor_client_->start_plan_execution(plan.value())){
        RCLCPP_ERROR(this->get_logger(), "Error starting a new plan (first)");

        return false;
    }

    return true;
}

void TaskControllerNode::init_knowledge(){
    const std::string robot_name = "tars";
    const std::string zones[6] = {"charging_station", "unload_zone", "reol_1", "reol_2", "reol_3", "reol_4"};
    const std::string pallets[4] = {"pallet_1", "pallet_2", "pallet_3", "pallet_4"};

    // add the robot and warehouse zones to the PDDL problem
    problem_expert_->addInstance(plansys2::Instance{robot_name, "robot"});

    for(const std::string &zone: zones){
        problem_expert_->addInstance(plansys2::Instance{zone, "zone"});
    }

    // set the robot's initial position and availability
    problem_expert_->addPredicate(plansys2::Predicate("(robot_at " + robot_name + " " + zones[0] + ")"));
    problem_expert_->addPredicate(plansys2::Predicate("(robot_available " + robot_name + ")"));

    // // set the different zones
    // problem_expert_->addPredicate(plansys2::Predicate("(is_charging_zone " + zones[0] + ")"));
    problem_expert_->addPredicate(plansys2::Predicate("(is_unload_zone " + zones[1] + ")"));

    for(int i = 2; i < 6; i++){
        problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone " + zones[i] + ")"));
    }

    // add pallets and set locations
    for(const std::string &pallet: pallets){
        problem_expert_->addInstance(plansys2::Instance{pallet, "pallet"});
        problem_expert_->addPredicate(plansys2::Predicate("(pallet_at " + pallet + " " + zones[1] + ")"));
        problem_expert_->addPredicate(plansys2::Predicate("(pallet_not_moved " + pallet + ")"));
    }

    // set the robot's goal
    problem_expert_->setGoal(plansys2::Goal(
        "(and(pallet_at " + pallets[0] + " " + zones[2] + ") " +
            "(pallet_at " + pallets[1] + " " + zones[3] + ") " +
            "(pallet_at " + pallets[2] + " " + zones[4] + ") " +
            "(pallet_at " + pallets[3] + " " + zones[5] + "))"
    ));
}

void TaskControllerNode::step(){
    if(!executor_client_->execute_and_check_plan()){
        auto result = executor_client_->getResult();
        if(result.value().success){
            RCLCPP_INFO(this->get_logger(), "Plan successfully finished");
        }else{
            RCLCPP_ERROR(this->get_logger(), "Plan finished with error");
        }
    }
}

int main(int argc, char **argv){
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TaskControllerNode>();

  if(!node->init()){
    return 0;
  }

  rclcpp::Rate rate(5);
  while(rclcpp::ok()){
    node->step();
    rate.sleep();

    rclcpp::spin_some(node->get_node_base_interface());
  }

  rclcpp::shutdown();
  
  return 0;
}

