#ifndef TASK_CONTROLLER_NODE_HPP
#define TASK_CONTROLLER_NODE_HPP

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "plansys2_executor/ExecutorClient.hpp"
#include "plansys2_problem_expert/ProblemExpertClient.hpp"
#include "plansys2_domain_expert/DomainExpertClient.hpp"
#include "plansys2_planner/PlannerClient.hpp"
#include "plansys2_msgs/msg/action_execution_info.hpp"
#include "plansys2_msgs/msg/plan.hpp"

class TaskControllerNode: public rclcpp::Node{
    public:
        TaskControllerNode(): rclcpp::Node("task_controller"){}

        // get domain, problem and plan and execute the plan
        bool initialize();

        // set instance, predicates and goal
        void initial_knowledge();
        void step();
    
    private:
        std::shared_ptr<plansys2::DomainExpertClient> domain_expert_;
        std::shared_ptr<plansys2::ProblemExpertClient> problem_expert_;
        std::shared_ptr<plansys2::PlannerClient> planner_client_;
        std::shared_ptr<plansys2::ExecutorClient> executor_client_;
};

#endif