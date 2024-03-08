#include "task_controller/bt_nodes/ApproachPallet.hpp"

namespace custom_bt_nodes{
    
    ApproachPallet::ApproachPallet(const std::string &xml_tag,
                                const BT::NodeConfiguration &configuration):
        BT::ActionNodeBase(xml_tag, configuration), counter_(0){}

    void ApproachPallet::halt(){
        std::cout << "ApproachPallet halt" << std::endl;
    }

    BT::NodeStatus ApproachPallet::tick(){
        std::cout << "Approaching pallet... " << counter_ << std::endl;

        if (counter_++ < 5) {
            return BT::NodeStatus::RUNNING;
        } else {
            counter_ = 0;
            std::cout << "Pallet approached." << std::endl;

            return BT::NodeStatus::SUCCESS;
        }
    }

} // end namespace custom_bt_nodes

BT_REGISTER_NODES(factory){
    factory.registerNodeType<custom_bt_nodes::ApproachPallet>("ApproachPallet");
}