#ifndef APPROACHPALLET_HPP
#define APPROACHPALLET_HPP

#include <string>

#include "behaviortree_cpp_v3/behavior_tree.h"
#include "behaviortree_cpp_v3/bt_factory.h"

// only a placeholder class

// To be implemented later //

class ApproachPallet: public BT::ActionNodeBase{
    public:
        explicit ApproachPallet(const std::string &xml_tag,
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