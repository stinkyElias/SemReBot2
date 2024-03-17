#include "semrebot2_lifecycle_manager/LifecycleManager.hpp"

namespace semrebot2{

LifecycleManager::LifecycleManager(
  const std::string &node_name, const std::string &managed_node):
        Node(node_name), managed_node_(managed_node) {}

void LifecycleManager::init(){
  std::string get_state_service_name = managed_node_ + "/get_state";
  std::string change_state_service_name = managed_node_ + "/change_state";

  client_get_state_ = this->create_client<lifecycle_msgs::srv::GetState>(get_state_service_name);
  client_change_state_ = this->create_client<lifecycle_msgs::srv::ChangeState>(change_state_service_name);

  RCLCPP_INFO(this->get_logger(), "Creating client for service %s", get_state_service_name.c_str());
  RCLCPP_INFO(this->get_logger(), "Creating client for service %s", change_state_service_name.c_str());
}

uint8_t LifecycleManager::get_state(std::chrono::seconds timeout){
    auto request = std::make_shared<lifecycle_msgs::srv::GetState::Request>();

    // check if service is up and running
    if(!client_get_state_->wait_for_service(timeout)){
        RCLCPP_ERROR(this->get_logger(), "Service %s is not available", client_get_state_->get_service_name());

        return lifecycle_msgs::msg::State::PRIMARY_STATE_UNKNOWN;
    }

    // get current state of the managed node
    auto future_result = client_get_state_->async_send_request(request);
    auto future_status = wait_for_result(future_result, timeout);
    auto state = future_result.get();

    // handle timeout
    if(future_status != std::future_status::ready){
        RCLCPP_ERROR(this->get_logger(), "Server timed out while getting current state of node %s",
                                            managed_node_.c_str());

        return lifecycle_msgs::msg::State::PRIMARY_STATE_UNKNOWN;        
    }

    // alert current state
    if(state != nullptr){
        RCLCPP_INFO(this->get_logger(), "%s has current state %s", get_name(), state->current_state.label.c_str());

        return state->current_state.id;
    }else{
        RCLCPP_ERROR(this->get_logger(), "Failed to get current state of %s", managed_node_.c_str());
        
        return lifecycle_msgs::msg::State::PRIMARY_STATE_UNKNOWN;
    }
}

bool LifecycleManager::change_state(uint8_t transition, std::chrono::seconds timeout){
    auto request = std::make_shared<lifecycle_msgs::srv::ChangeState::Request>();
    request->transition.id = transition;

    if(!client_change_state_->wait_for_service(timeout)){
        RCLCPP_ERROR(this->get_logger(), "Service %s is not available", client_change_state_->get_service_name());

        return false;
    }

    auto future_result = client_change_state_->async_send_request(request);
    auto future_status = wait_for_result(future_result, timeout);

    if(future_status != std::future_status::ready){
        RCLCPP_ERROR(this->get_logger(), "Server timed out while getting current state of %s", managed_node_.c_str());

        return false;
    }

    if(future_result.get()->success){
        RCLCPP_INFO(this->get_logger(), "Transition %u was successful", transition);

        return true;
    }else{
        RCLCPP_WARN(this->get_logger(), "Transition %u unsuccessful", transition);

        return false;
    }
}

bool startup_function(std::map<std::string, std::shared_ptr<LifecycleManager>> &manager_nodes,
                        std::chrono::seconds timeout){
    // whisper
    if(!manager_nodes["whisper"]->change_state(lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE, timeout)){
        return false;
    }

    while(manager_nodes["whisper"]->get_state() != lifecycle_msgs::msg::State::PRIMARY_STATE_INACTIVE){
        std::cerr << "Waiting for whisper to be inactive" << std::endl;
    }

    // mistral
    if(!manager_nodes["mistral"]->change_state(lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE, timeout)){
        return false;
    }

    while(manager_nodes["mistral"]->get_state() != lifecycle_msgs::msg::State::PRIMARY_STATE_INACTIVE){
        std::cerr << "Waiting for mistral to be inactive" << std::endl;
    }

    // activate
    if(!rclcpp::ok()){
        return false;
    }

    if(!manager_nodes["whisper"]->change_state(lifecycle_msgs::msg::Transition::TRANSITION_ACTIVATE, timeout)){
        return false;
    }

    if(!manager_nodes["mistral"]->change_state(lifecycle_msgs::msg::Transition::TRANSITION_ACTIVATE, timeout)){
        return false;
    }

    if(!manager_nodes["whisper"]->get_state()){
        return false;
    }

    if(!manager_nodes["mistral"]->get_state()){
        return false;
    }

    return true;
}

} // end namespace semrebot2