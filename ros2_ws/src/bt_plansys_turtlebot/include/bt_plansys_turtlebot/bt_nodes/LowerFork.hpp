#ifndef LOWERFORK_HPP
#define LOWERFORK_HPP

#include <string>

#include "behaviortree_cpp_v3/behavior_tree.h"
#include "behaviortree_cpp_v3/bt_factory.h"

class LowerFork: public BT::ActionNodeBase{
    public:
        explicit LowerFork(const std::string &xml_tag,
                           const BT::NodeConfiguration &config);

        void halt();
        BT::NodeStatus tick();

        static BT::PortsList providedPorts(){
            return BT::PortsList({});
        }

    private:
        int counter_;
};

#endif