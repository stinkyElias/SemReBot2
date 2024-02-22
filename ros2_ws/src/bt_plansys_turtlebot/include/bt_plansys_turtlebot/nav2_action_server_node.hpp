// #ifndef NAV2_ACTION_SERVER_NODE_HPP
// #define NAV2_ACTION_SERVER_NODE_HPP

// #include <memory>

// #include "rclcpp/rclcpp.hpp"
// #include "rclcpp_action/rclcpp_action.hpp"
// #include "nav2_msgs/action/navigate_to_pose.hpp"
// #include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"

// class Nav2ActionServerNode : public rclcpp::Node
// {
//     public:
//         Nav2ActionServerNode(): Node("navigate_to_pose_server"){}
//         void start_server();
    
//     private:
//         rclcpp_action::Server<nav2_msgs::action::NavigateToPose>::SharedPtr action_server_;
//         nav2_msgs::action::NavigateToPose::Goal goal_;

//         rclcpp_action::GoalResponse handle_goal(
//             const rclcpp_action::GoalUUID &uuid,
//             std::shared_ptr<const nav2_msgs::action::NavigateToPose::Goal> goal);

//         rclcpp_action::CancelResponse handle_cancel(
//             const std::shared_ptr<rclcpp_action::ServerGoalHandle   
//             <nav2_msgs::action::NavigateToPose>> goal_handle);

//         void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle
//             <nav2_msgs::action::NavigateToPose>> goal_handle);
        
//         void handle_accepted(const std::shared_ptr<rclcpp_action::ServerGoalHandle
//             <nav2_msgs::action::NavigateToPose>> goal_handle);

// };

// #endif