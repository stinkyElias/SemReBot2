#include <iostream>

#include "bt_plansys_turtlebot/bt_nodes/Recharge.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"

// constructer passing BT tag and configuration to ActionNodeBase
Recharge::Recharge(const std::string &xml_tag,
                   const BT::NodeConfiguration &configuration):
                   BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

// denne funksjonen må endres slik at vi bruker RCLCPP_INFO
void Recharge::halt(){
    // rclcpp_lifecycle::LifecycleNode::SharedPtr ros_node;
    // RCLCPP_INFO(this->get_logger(), "Recharge halt");
    std::cout << "Recharge halt" << std::endl;
}

BT::NodeStatus Recharge::tick(){
    std::cout << "Recharge tick" << counter_ << std::endl;

    if(counter_++ < 10){
        return BT::NodeStatus::RUNNING;
    }else{
        counter_ = 0;
        
        return BT::NodeStatus::SUCCESS;
    }
}

BT_REGISTER_NODES(factory){
    factory.registerNodeType<Recharge>("Recharge");
}