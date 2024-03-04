#include <vector>
#include <memory>

#include "bt_plansys_turtlebot/bt_nodes/Navigate.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"

namespace std{

Navigate::Navigate(const string &xml_tag,
                   const string &action_name,
                   const BT::NodeConfiguration &configuration):

    // passing tag, action and config to BtActionNode using Nav2
    plansys2::BtActionNode<nav2_msgs::action::NavigateToPose>(xml_tag,
                                                              action_name,
                                                              configuration)
{
    // Get node from BT blackboard and store a shared pointer to it
    // in node. Allows access the node elsewhere in the code.
    rclcpp_lifecycle::LifecycleNode::SharedPtr ros_node;
    if(!BT::TreeNode::config().blackboard->get("node", ros_node)){
        RCLCPP_ERROR(node_->get_logger(), "Failed to get 'node' from blackboard.");
    }

    try{
        ros_node->declare_parameter<vector<string>>("waypoints");
    } catch (const rclcpp::exceptions::ParameterAlreadyDeclaredException &e){
        // pass
    }

    // set waypoint parameters
    if(ros_node->has_parameter("waypoints")){
        vector<string> waypoint_names;
        ros_node->get_parameter_or("waypoints", waypoint_names, {});

        for(auto &waypoint: waypoint_names){
            try{
                ros_node->declare_parameter<vector<double>>("waypoint_coordinates." + waypoint);
            }catch (const rclcpp::exceptions::ParameterAlreadyDeclaredException &e){
                // pass
            }

            vector<double> coordinates;
            if(ros_node->get_parameter_or("waypoint_coordinates." + waypoint, coordinates, {})){
                geometry_msgs::msg::Pose2D pose;

                pose.x = coordinates[0];
                pose.y = coordinates[1];
                pose.theta = coordinates[2];

                this->waypoints_[waypoint] = pose;

            }else{
                // RCLCPP_ERROR(ros_node->get_logger(), ("No coordinate exist for waypoint " + waypoint).c_str());
                cerr << "No coordinates exist for waypoint " << waypoint << endl;
            }
        }
    }
}

BT::NodeStatus Navigate::on_tick(){
    // tick leaf node and set status to running if it is not already
    if(status() == BT::NodeStatus::IDLE){
        rclcpp_lifecycle::LifecycleNode::SharedPtr ros_node;
        if(!BT::TreeNode::config().blackboard->get("node", ros_node)){
            RCLCPP_ERROR(node_->get_logger(), "Failed to get 'node' from blackboard.");
        }

        // get coordinates of the goal from blackboard and store in end_pose
        string end_pose;
        BT::TreeNode::getInput<string>("goal", end_pose);

        // get coordinates of the goal from waypoints_ and store in pose
        geometry_msgs::msg::Pose2D pose;
        if(this->waypoints_.find(end_pose) != this->waypoints_.end()){
            pose = this->waypoints_[end_pose];
        }else{
            // RCLCPP_ERROR(ros_node->get_logger(), ("No coordiante for waypoint" + end_pose).c_str());
            cerr << "No coordinate exist for waypoint " << end_pose << endl;
        }

        // set goal pose (2D pose)
        geometry_msgs::msg::PoseStamped goal_pose;

        goal_pose.header.frame_id = "map";
        goal_pose.header.stamp = ros_node->now();

        goal_pose.pose.position.x = pose.x;
        goal_pose.pose.position.y = pose.y;
        goal_pose.pose.position.z = 0.0;

        // set orientation around z axis (yaw) with quaternion representation
        goal_pose.pose.orientation = tf2::toMsg(tf2::Quaternion({0.0, 0.0, 1.0}, pose.theta));
    
        goal_.pose = goal_pose;
    }
    
    return BT::NodeStatus::RUNNING;
}

BT::NodeStatus Navigate::on_success(){
    return BT::NodeStatus::SUCCESS;
}

// register Move node to BT factory
BT_REGISTER_NODES(factory){
    BT::NodeBuilder builder = [](const string &name,
                                 const BT::NodeConfiguration &configuration)
        {
            return make_unique<Navigate>(name, "navigate_to_pose", configuration);
        };
    
    factory.registerBuilder<Navigate>("Navigate", builder);
}

} // end namespace std