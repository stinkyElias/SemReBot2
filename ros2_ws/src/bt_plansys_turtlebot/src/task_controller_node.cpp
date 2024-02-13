#include "bt_plansys_turtlebot/task_controller_node.hpp"

bool TaskControllerNode::initialize(){
    domain_expert_ = std::make_shared<plansys2::DomainExpertClient>();
    problem_expert_ = std::make_shared<plansys2::ProblemExpertClient>();
    planner_client_ = std::make_shared<plansys2::PlannerClient>();
    executor_client_ = std::make_shared<plansys2::ExecutorClient>();

    this->initial_knowledge();

    auto domain = domain_expert_->getDomain();
    auto problem = problem_expert_->getProblem();
    auto plan = planner_client_->getPlan(domain, problem);

    if(!plan.has_value()){
        RCLCPP_ERROR(this->get_logger(), ("Could not find a plan to reach goal " +
            parser::pddl::toString(problem_expert_->getGoal())).c_str());
        
        return false;
    }

    if(!executor_client_->start_plan_execution(plan.value())){
        RCLCPP_WARN(this->get_logger(), "Error starting a new plan execution.");
    }

    return true;
}

void TaskControllerNode::initial_knowledge(){
    // add instances
    problem_expert_->addInstance(plansys2::Instance{"turtle", "robot"});

    problem_expert_->addInstance(plansys2::Instance{"recharge_station", "zone"});
    problem_expert_->addInstance(plansys2::Instance{"unload_zone", "zone"});
    problem_expert_->addInstance(plansys2::Instance{"reol_1", "zone"});
    problem_expert_->addInstance(plansys2::Instance{"reol_2", "zone"});
    problem_expert_->addInstance(plansys2::Instance{"reol_3", "zone"});
    problem_expert_->addInstance(plansys2::Instance{"reol_4", "zone"});

    problem_expert_->addInstance(plansys2::Instance{"pallet_1", "pallet"});
    problem_expert_->addInstance(plansys2::Instance{"pallet_2", "pallet"});
    problem_expert_->addInstance(plansys2::Instance{"pallet_3", "pallet"});
    problem_expert_->addInstance(plansys2::Instance{"pallet_4", "pallet"});

    // add predicates
    problem_expert_->addPredicate(plansys2::Predicate("(is_recharge_zone recharge_station)"));
    problem_expert_->addPredicate(plansys2::Predicate("(is_unload_zone unload_zone)"));

    problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone reol_1)"));
    problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone reol_2)"));
    problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone reol_3)"));
    problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone reol_4)"));

    problem_expert_->addPredicate(plansys2::Predicate("(pallet_at pallet_1 unload_zone)"));
    problem_expert_->addPredicate(plansys2::Predicate("(pallet_at pallet_2 unload_zone)"));
    problem_expert_->addPredicate(plansys2::Predicate("(pallet_at pallet_3 unload_zone)"));
    problem_expert_->addPredicate(plansys2::Predicate("(pallet_at pallet_4 unload_zone)"));

    problem_expert_->addPredicate(plansys2::Predicate("(robot_at turtle recharge_station)"));
    problem_expert_->addPredicate(plansys2::Predicate("(battery_full turtle)"));
    problem_expert_->addPredicate(plansys2::Predicate("(robot_available turtle)"));

    problem_expert_->addPredicate(plansys2::Predicate("(pallet_not_moved pallet_1)"));
    problem_expert_->addPredicate(plansys2::Predicate("(pallet_not_moved pallet_2)"));
    problem_expert_->addPredicate(plansys2::Predicate("(pallet_not_moved pallet_3)"));
    problem_expert_->addPredicate(plansys2::Predicate("(pallet_not_moved pallet_4)"));

    // set goal
    problem_expert_->setGoal(plansys2::Goal(
        "(and (pallet_at pallet_1 reol_2) (pallet_at pallet_2 reol_4) (pallet_at pallet_3 reol_1) (pallet_at pallet_4 reol_3))"
    ));
}

void TaskControllerNode::step(){
    if(!executor_client_->execute_and_check_plan()){
        auto result = executor_client_->getResult();

        if(result.value().success){
            RCLCPP_INFO(this->get_logger(), "Plan finished successfully");
        }else{
            RCLCPP_ERROR(this->get_logger(), "Plan finished with error");
        }
    }
}

int main(int argc, char **argv){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TaskControllerNode>();

    if(!node->initialize()){
        return 0;
    }

    rclcpp::Rate rate(5);
    while(rclcpp::ok()){
        node->step();
        rate.sleep();
        rclcpp::spin_some(node->get_node_base_interface());
    }

    rclcpp::shutdown();
}