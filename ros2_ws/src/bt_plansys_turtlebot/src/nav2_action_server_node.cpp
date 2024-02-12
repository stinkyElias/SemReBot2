#include "bt_plansys_turtlebot/nav2_action_server_node.hpp"

void Nav2ActionServerNode::start_server(){
  action_server_ = rclcpp_action::create_server<nav2_msgs::action::NavigateToPose>
  (
    shared_from_this(),
    "navigate_to_pose",
    std::bind(&Nav2ActionServerNode::handle_goal, this, std::placeholders::_1,
                                                        std::placeholders::_2),
    std::bind(&Nav2ActionServerNode::handle_cancel, this, std::placeholders::_1),
    std::bind(&Nav2ActionServerNode::handle_accepted, this, std::placeholders::_1)
  );

    RCLCPP_INFO(this->get_logger(), "Action server ready.");
}

rclcpp_action::GoalResponse Nav2ActionServerNode::handle_goal(
  const rclcpp_action::GoalUUID &uuid,
  std::shared_ptr<const nav2_msgs::action::NavigateToPose::Goal> goal){
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

rclcpp_action::CancelResponse Nav2ActionServerNode::handle_cancel(
  const std::shared_ptr<rclcpp_action::ServerGoalHandle
  <nav2_msgs::action::NavigateToPose>> goal_handle){
    RCLCPP_INFO(this->get_logger(), "Canceling current goal.");

    return rclcpp_action::CancelResponse::ACCEPT;
  }

void Nav2ActionServerNode::handle_accepted(const std::shared_ptr
<rclcpp_action::ServerGoalHandle<nav2_msgs::action::NavigateToPose>> goal_handle){
  std::thread{std::bind(&Nav2ActionServerNode::execute, this, std::placeholders::_1),
              goal_handle}.detach();
}

void Nav2ActionServerNode::execute(const std::shared_ptr
<rclcpp_action::ServerGoalHandle<nav2_msgs::action::NavigateToPose>> goal_handle){
  rclcpp::Rate loop_rate(1);
  auto feedback = std::make_shared<nav2_msgs::action::NavigateToPose::Feedback>();
  auto result = std::make_shared<nav2_msgs::action::NavigateToPose::Result>();

  auto pose_cmd = goal_handle->get_goal()->pose.pose;

  tf2::Quaternion quaternion;
  tf2::fromMsg(pose_cmd.orientation, quaternion);

  RCLCPP_INFO(this->get_logger(), "Navigating to %lf, %lf, %lf", pose_cmd.position.x,
                                                                 pose_cmd.position.y,
                                                                 quaternion.getAngle());
  auto start = this->now();
  int current_times = 0;

  while(rclcpp::ok() && current_times++ < 10){
    RCLCPP_INFO(this->get_logger(), "Navigating %d ", current_times);

    if(goal_handle->is_canceling()){
      goal_handle->canceled(result);

      RCLCPP_INFO(this->get_logger(), "Action canceled.");

      return;
    }

    loop_rate.sleep();
  }

  if(rclcpp::ok()){
    goal_handle->succeed(result);

    RCLCPP_INFO(this->get_logger(), "Navigation succeeded.");
  }
}

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<Nav2ActionServerNode>();
  node->start_server();

  rclcpp::spin(node);

  rclcpp::shutdown();
  
  return 0;
}
