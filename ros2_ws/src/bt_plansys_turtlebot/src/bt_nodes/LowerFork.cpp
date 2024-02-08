#include <iostream>

#include "bt_plansys_turtlebot/bt_nodes/LowerFork.hpp"

LowerFork::LowerFork(const std::string &xml_tag,
                     const BT::NodeConfiguration &configuration):
                     BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

void LowerFork::halt(){
    std::cout << "LowerFork halt" << std::endl;
}

BT::NodeStatus LowerFork::tick(){
    std::cout << "LowerFork tick" << counter_ << std::endl;

    if(counter_++ < 5){
        return BT::NodeStatus::RUNNING;
    }else{
        counter_ = 0;
        
        return BT::NodeStatus::SUCCESS;
    }
}

// Register node as LowerFork
BT_REGISTER_NODES(factory){
    factory.registerNodeType<LowerFork>("LowerFork");
}