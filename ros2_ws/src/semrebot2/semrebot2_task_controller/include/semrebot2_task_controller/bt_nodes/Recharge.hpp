#ifndef SEMREBOT2_RECHARGE_HPP
#define SEMREBOT2_RECHARGE_HPP

#include <string>
#include <iostream>

#include "behaviortree_cpp/behavior_tree.h"
#include "behaviortree_cpp/bt_factory.h"

class Recharge: public BT::ActionNodeBase{
    public:
        explicit Recharge(
            const std::string &xml_name,
            const BT::NodeConfiguration &configuration
        );

        void halt();
        BT::NodeStatus tick();

        static BT::PortsList providedPorts(){
            return BT::PortsList({});
        }
    
    private:
        int counter_;
};

#endif // SEMREBOT2_RECHARGE_HPP