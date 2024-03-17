#include "semrebot2_task_controller/bt_nodes/LowerFork.hpp"

namespace custom_bt_nodes{

    LowerFork::LowerFork(const std::string &xml_tag,
                         const BT::NodeConfiguration &configuration):
        BT::ActionNodeBase(xml_tag, configuration), counter_(0){}
    
    void LowerFork::halt(){
        std::cout << "LowerFork halt" << std::endl;
    }

    BT::NodeStatus LowerFork::tick(){
        std::cout << "Lowering fork... " << counter_ << std::endl;

        if (counter_++ < 5) {
            return BT::NodeStatus::RUNNING;
        } else {
            counter_ = 0;
            std::cout << "Fork lowered." << std::endl;

            return BT::NodeStatus::SUCCESS;
        }
    }

} // end namespace custom_bt_nodes

BT_REGISTER_NODES(factory){
    factory.registerNodeType<custom_bt_nodes::LowerFork>("LowerFork");
}