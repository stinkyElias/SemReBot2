#ifndef SEMREBOT2_TASK_CONTROLLER_NODE_HPP
#define SEMREBOT2_TASK_CONTROLLER_NODE_HPP

#include <memory>
#include <string>
#include <iterator>
#include <chrono>
#include <vector>

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

namespace semrebot2{

class TaskControllerNode: public rclcpp::Node{
    public:
        TaskControllerNode();

        bool get_plan_logic_and_start();
        void get_problem_specific_knowledge(std::string &command);

        double get_distance(std::string from_zone, std::string to_zone);
        // void set_duration();
        void set_hardcoded_speed_and_distance();
    
    private:
        std::shared_ptr<plansys2::DomainExpertClient> domain_expert_;
        std::shared_ptr<plansys2::ProblemExpertClient> problem_expert_;
        std::shared_ptr<plansys2::PlannerClient> planner_client_;
        std::shared_ptr<plansys2::ExecutorClient> executor_client_;

        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
        std::string message_;

        const std::string robot_name_{"tars"};
        const std::string zones_[6] = {"charging_station", "unload_zone",
                                    "shelf_1", "shelf_2", "shelf_3", "shelf_4"};
        std::string robot_start_location;

        // values for PDDL functions
        const std::string robot_speed_{"0.26"};   // m/s - from Turtlebot3 manual
        std::map<std::string, std::vector<double>> waypoint_coordinates_;
        std::string battery_level{"100"};

        /////////////////////////////////////////////////////////////////
        // for testing
        std::chrono::_V2::system_clock::time_point start_time_callback;
        std::chrono::_V2::system_clock::time_point start_time_planner;
        std::chrono::_V2::system_clock::time_point end_time;
        std::chrono::duration<double> elapsed_time_callback;
        std::chrono::duration<double> elapsed_time_planner;
        /////////////////////////////////////////////////////////////////
};

} // end namespace semrebot2

#endif // SEMREBOT2_TASK_CONTROLLER_NODE_HPP