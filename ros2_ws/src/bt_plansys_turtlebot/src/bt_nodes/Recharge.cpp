#include "bt_plansys_turtlebot/bt_nodes/Recharge.hpp"

Recharge::Recharge(const std::string &xml_name,
                   const BT::NodeConfiguration &configuration):
    BT::ActionNodeBase(xml_name, configuration){
        counter_ = 0;
}

void Recharge::halt(){
    std::cout << "Recharge halt" << std::endl;
}

BT::NodeStatus Recharge::tick(){
    std::cout << "Recharge tick " << this->counter_ << std::endl;

    if(this->counter_++ < 10){
        return BT::NodeStatus::RUNNING;
    }else{
        this->counter_ = 0;
        return BT::NodeStatus::SUCCESS;
    }
}

BT_REGISTER_NODES(factory){
    factory.registerNodeType<Recharge>("Recharge");
}
