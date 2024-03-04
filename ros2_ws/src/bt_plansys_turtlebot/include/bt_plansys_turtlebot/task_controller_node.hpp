#ifndef TASK_CONTROLLER_NODE_HPP
#define TASK_CONTROLLER_NODE_HPP

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "plansys2_domain_expert/DomainExpertClient.hpp"
#include "plansys2_executor/ExecutorClient.hpp"
#include "plansys2_planner/PlannerClient.hpp"
#include "plansys2_problem_expert/ProblemExpertClient.hpp"

class TaskControllerNode: public rclcpp::Node{
    public:
        TaskControllerNode();
    
        bool init();
        void init_knowledge();
        void step();
    
    private:
        std::shared_ptr<plansys2::DomainExpertClient> domain_expert_;
        std::shared_ptr<plansys2::ProblemExpertClient> problem_expert_;
        std::shared_ptr<plansys2::PlannerClient> planner_client_;
        std::shared_ptr<plansys2::ExecutorClient> executor_client_;
};

#endif // TASK_CONTROLLER_NODE_HPP