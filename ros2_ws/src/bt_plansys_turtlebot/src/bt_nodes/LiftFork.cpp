#include <iostream>

#include "bt_plansys_turtlebot/bt_nodes/LiftFork.hpp"

LiftFork::LiftFork(const std::string &xml_tag,
                   const BT::NodeConfiguration &configuration):
                   BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

void LiftFork::halt(){
    std::cout << "LiftFork halt" << std::endl;
}

BT::NodeStatus LiftFork::tick(){
    std::cout << "LiftFork tick" << counter_ << std::endl;

    if(counter_++ < 5){
        return BT::NodeStatus::RUNNING;
    }else{
        counter_ = 0;
        
        return BT::NodeStatus::SUCCESS;
    }
}

BT_REGISTER_NODES(factory){
    factory.registerNodeType<LiftFork>("LiftFork");
}
