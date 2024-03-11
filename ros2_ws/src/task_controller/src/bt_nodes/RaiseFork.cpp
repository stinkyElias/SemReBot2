#include "task_controller/bt_nodes/RaiseFork.hpp"

namespace custom_bt_nodes{

    RaiseFork::RaiseFork(const std::string &xml_tag,
                         const BT::NodeConfiguration &configuration):
        BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

    void RaiseFork::halt(){
        std::cout << "RaiseFork halt" << std::endl;
    }

    BT::NodeStatus RaiseFork::tick(){
        std::cout << "Raising fork... " << counter_ << std::endl;

        if (counter_++ < 5) {
            return BT::NodeStatus::RUNNING;
        } else {
            counter_ = 0;
            std::cout << "Fork raised." << std::endl;

            return BT::NodeStatus::SUCCESS;
        }
    }

} // end namespace custom_bt_nodes

BT_REGISTER_NODES(factory){
    factory.registerNodeType<custom_bt_nodes::RaiseFork>("RaiseFork");
}