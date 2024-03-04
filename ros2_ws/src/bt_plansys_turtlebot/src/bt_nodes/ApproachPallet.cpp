#include "bt_plansys_turtlebot/bt_nodes/ApproachPallet.hpp"

ApproachPallet::ApproachPallet(const std::string &xml_tag,
                               const BT::NodeConfiguration &configuration):
    BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

void ApproachPallet::halt(){
    std::cout << "ApproachPallet halt" << std::endl;
}

BT::NodeStatus ApproachPallet::tick(){
    std::cout << "ApproachPallet tick " << counter_ << std::endl;

    if (counter_++ < 5) {
        return BT::NodeStatus::RUNNING;
    } else {
        counter_ = 0;
        return BT::NodeStatus::SUCCESS;
    }
}

BT_REGISTER_NODES(factory){
    factory.registerNodeType<ApproachPallet>("ApproachPallet");
}