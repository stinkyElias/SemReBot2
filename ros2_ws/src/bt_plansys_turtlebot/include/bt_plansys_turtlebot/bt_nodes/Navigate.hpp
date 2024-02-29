#ifndef NAVIGATE_HPP
#define NAVIGATE_HPP

#include <string>
#include <map>

#include "geometry_msgs/msg/pose2_d.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"
#include "plansys2_bt_actions/BTActionNode.hpp"

#include "behaviortree_cpp/behavior_tree.h"
#include "behaviortree_cpp/bt_factory.h"

class Navigate: public plansys2::BtActionNode<nav2_msgs::action::NavigateToPose>{
    public:
        // Constructor taking the BT tag (XML file), node to be executed
        // in the tree and the configuration of the node on how to execute it.
        explicit Navigate(const std::string &xml_tag,
                      const std::string &action_name,
                      const BT::NodeConfiguration &configuration);
        
        // What the node does when ticked
        BT::NodeStatus on_tick() override;
        
        // What the node does when it succeeds
        BT::NodeStatus on_success() override;
        
        // Create an input port so that the node can receive the goal
        // to navigate to.
        static BT::PortsList providedPorts(){
            return {BT::InputPort<std::string>("goal")};
        }
    
    private:
        int goal_reached_;
        std::map<std::string, geometry_msgs::msg::Pose2D> waypoints_;
};

#endif