#ifndef SEMREBOT2_LIFECYCLE_MANAGER_HPP
#define SEMBREBOT2_LIFECYCLE_MANAGER_HPP

#include <chrono>
#include <memory>
#include <string>
#include <map>

#include "rclcpp/rclcpp.hpp"
#include "lifecycle_msgs/msg/state.hpp"
#include "lifecycle_msgs/msg/transition.hpp"
#include "lifecycle_msgs/srv/change_state.hpp"
#include "lifecycle_msgs/srv/get_state.hpp"

namespace semrebot2{

template<typename FutureT, typename WaitTimeT> std::future_status wait_for_result(FutureT &future,
                                                                                WaitTimeT time_to_wait){
    auto end = std::chrono::steady_clock::now() + time_to_wait;
    std::chrono::milliseconds wait_period(100);
    std::future_status status = std::future_status::timeout;

    do{
        auto now = std::chrono::steady_clock::now();
        auto time_left = end - now;

        if(time_left <= std::chrono::seconds(0)){
            break;
        }

        status = future.wait_for((time_left < wait_period) ? time_left : wait_period);
    } while(rclcpp::ok() && status != std::future_status::ready);

    return status;
}

class LifecycleManager: public rclcpp::Node{
    public:
        explicit LifecycleManager(const std::string &node_name,
                                const std::string &managed_node);
        void init();
        uint8_t get_state(std::chrono::seconds time_out = std::chrono::seconds(30));
        bool change_state(std::uint8_t transition,
                        std::chrono::seconds time_out = std::chrono::seconds(30));
    private:
        std::shared_ptr<rclcpp::Client<lifecycle_msgs::srv::GetState>> client_get_state_;
        std::shared_ptr<rclcpp::Client<lifecycle_msgs::srv::ChangeState>> client_change_state_;
        std::string managed_node_;
};

bool startup_function(std::map<std::string, std::shared_ptr<LifecycleManager>> &manager_nodes,
                    std::chrono::seconds timeout);

} // end namespace semrebot2

#endif // SEMREBOT2_LIFECYCLE_MANAGER_HPP