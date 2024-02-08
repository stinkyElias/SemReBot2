#ifndef LIFTFORK_HPP
#define LIFTFORK_HPP

#include <string>

#include "behaviortree_cpp_v3/behavior_tree.h"
#include "behaviortree_cpp_v3/bt_factory.h"

class LiftFork: public BT::ActionNodeBase{
    public:
        explicit LiftFork(const std::string &xml_tag,
                          const BT::NodeConfiguration &configuration);

        void halt();
        BT::NodeStatus tick();

        static BT::PortsList providedPorts(){
            return BT::PortsList({});
        }

    private:
        int counter_;
};

#endif