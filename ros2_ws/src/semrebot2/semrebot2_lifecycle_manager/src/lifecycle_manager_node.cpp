#include "semrebot2_lifecycle_manager/LifecycleManager.hpp"

int main(int argc, char **argv)
{
  setvbuf(stdout, NULL, _IONBF, BUFSIZ);

  rclcpp::init(argc, argv);

  std::map<std::string, std::shared_ptr<semrebot2::LifecycleManager>> manager_nodes;
  manager_nodes["whisper"] = std::make_shared<semrebot2::LifecycleManager>("whisper_lc_mngr", "whisper");
  manager_nodes["mistral"] = std::make_shared<semrebot2::LifecycleManager>("mistral_lc_mngr", "mistral");

  rclcpp::executors::SingleThreadedExecutor executor;
  for(auto &manager_node: manager_nodes){
    manager_node.second->init();
    executor.add_node(manager_node.second);
  }

  std::shared_future<bool> startup_future = std::async(
    std::launch::async,
    std::bind(semrebot2::startup_function, manager_nodes, std::chrono::seconds(30)));

  executor.spin_until_future_complete(startup_future);

  if(!startup_future.get()){
    RCLCPP_ERROR(rclcpp::get_logger("semrebot2_lifecycle_manager"), "Failed to start SemReBot2");

    rclcpp::shutdown();
    return -1;
  }

  rclcpp::shutdown();

  return 0;
}