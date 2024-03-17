#include "semrebot2_task_controller/bt_nodes/LeavePallet.hpp"

namespace custom_bt_nodes{

    LeavePallet::LeavePallet(const std::string &xml_tag,
                            const BT::NodeConfiguration &configuration):
        BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

    void LeavePallet::halt(){
        std::cout << "LeavePallet halt" << std::endl;
    }

    BT::NodeStatus LeavePallet::tick(){
        std::cout << "Leaving pallet... " << counter_ << std::endl;

        if (counter_++ < 5) {
            return BT::NodeStatus::RUNNING;
        } else {
            counter_ = 0;
            std::cout << "Pallet left." << std::endl;

            return BT::NodeStatus::SUCCESS;
        }
    }

} // end namespace custom_bt_nodes

BT_REGISTER_NODES(factory){
    factory.registerNodeType<custom_bt_nodes::LeavePallet>("LeavePallet");
}