#ifndef TASK_CONTROLLER_NODE_HPP
#define TASK_CONTROLLER_NODE_HPP

#include <memory>
#include <string>
#include <mutex>
#include <condition_variable>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "std_msgs/msg/string.hpp"
#include "plansys2_domain_expert/DomainExpertClient.hpp"
#include "plansys2_executor/ExecutorClient.hpp"
#include "plansys2_planner/PlannerClient.hpp"
#include "plansys2_problem_expert/ProblemExpertClient.hpp"
#include "plansys2_msgs/msg/action_execution_info.hpp"
#include "plansys2_msgs/msg/plan.hpp"
#include "plansys2_pddl_parser/Utils.h"

class TaskControllerNode: public rclcpp::Node{
    public:
        TaskControllerNode();

        bool get_plan_logic_and_start();
        void get_problem_specific_knowledge(std::string &command);
        // bool init();
        // void init_knowledge();
        // void new_knowledge(std::string &command);
        // void step();
    
    private:
        std::shared_ptr<plansys2::DomainExpertClient> domain_expert_;
        std::shared_ptr<plansys2::ProblemExpertClient> problem_expert_;
        std::shared_ptr<plansys2::PlannerClient> planner_client_;
        std::shared_ptr<plansys2::ExecutorClient> executor_client_;

        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
        std::string message_;

        std::mutex command_mutex_;
        std::condition_variable condition_variable_;
        bool received_command_{false};

        const std::string robot_name_{"tars"};
        const std::string zones_[6] = {"charging_station", "unload_zone",
                                       "reol_1", "reol_2", "reol_3", "reol_4"};
        std::string robot_start_location;
};

#endif // TASK_CONTROLLER_NODE_HPP