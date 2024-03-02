#include "bt_plansys_turtlebot/navigate_node.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "plansys2_msgs/msg/action_execution_info.hpp"
#include "plansys2_msgs/msg/plan.hpp"
#include "plansys2_pddl_parser/Utils.h"

NavigateNode::NavigateNode(): rclcpp::Node("navigate_node"){}

bool NavigateNode::init(){
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

    if(!executor_client_->start_plan_execution(plan.value())){
        RCLCPP_ERROR(this->get_logger(), "Error starting a new plan (first)");

        return false;
    }

    return true;
}

void NavigateNode::init_knowledge(){
    std::string robot_name = "r2d2";
    std::string zones[6] = {"charging_station", "unload_zone", "reol_1", "reol_2", "reol_3", "reol_4"};
    
    // add the robot and warehouse zones to the PDDL problem
    problem_expert_->addInstance(plansys2::Instance{robot_name, "robot"});

    for(const std::string &zone: zones){
        problem_expert_->addInstance(plansys2::Instance{zone, "zone"});
    }

    // set the robot's initial position, battery capacity and availability
    problem_expert_->addPredicate(plansys2::Predicate("(robot_at " + robot_name + " " + zones[0] + ")"));
    problem_expert_->addPredicate(plansys2::Predicate("(robot_available " + robot_name + ")"));
    problem_expert_->addPredicate(plansys2::Predicate("(battery_full " + robot_name + ")"));

    // set the robot's goal
    problem_expert_->setGoal(plansys2::Goal("(and(robot_at " + robot_name + " " + zones[1] + "))"));
    
}

void NavigateNode::step(){
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
  auto node = std::make_shared<NavigateNode>();

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

