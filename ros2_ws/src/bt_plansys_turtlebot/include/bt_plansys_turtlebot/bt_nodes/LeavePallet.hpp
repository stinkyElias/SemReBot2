#ifndef LEAVE_PALLET_HPP
#define LEAVE_PALLET_HPP

#include <string>
#include <iostream>

#include "behaviortree_cpp/behavior_tree.h"
#include "behaviortree_cpp/bt_factory.h"

namespace custom_bt_nodes{

    class LeavePallet: public BT::ActionNodeBase{
        public:
            explicit LeavePallet(const std::string &xml_tag,
                                const BT::NodeConfiguration &configuration);
            void halt();
            BT::NodeStatus tick();

            static BT::PortsList providedPorts(){
                return BT::PortsList({});
            }

        private:
            int counter_;
    };

} // end namespace custom_bt_nodes

#endif // LEAVE_PALLET_HPP