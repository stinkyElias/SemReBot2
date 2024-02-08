#ifndef RECHARGE_HPP
#define RECHARGE_HPP

#include <string>

#include "behaviortree_cpp_v3/behavior_tree.h"
#include "behaviortree_cpp_v3/bt_factory.h"

class Recharge: public BT::ActionNodeBase{
    public:
        explicit Recharge(const std::string &xml_tag,
                        const BT::NodeConfiguration &configuration);
        
        void halt();

        // simulate recharging
        BT::NodeStatus tick();

        static BT::PortsList providedPorts(){
            return BT::PortsList({});
        }
    
    private:
        int counter_;
};

#endif