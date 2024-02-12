cmake_minimum_required(VERSION 3.8)
project(bt_plansys_turtlebot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_index_cpp REQUIRED)

find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(nav2_msgs REQUIRED)

find_package(plansys2_msgs REQUIRED)
find_package(plansys2_executor REQUIRED)
find_package(plansys2_domain_expert REQUIRED)
find_package(plansys2_problem_expert REQUIRED)
find_package(plansys2_planner REQUIRED)
find_package(plansys2_pddl_parser REQUIRED)
find_package(plansys2_bt_actions REQUIRED)

set(dependencies
    rclcpp
    rclcpp_action
    geometry_msgs
    tf2_geometry_msgs
    nav2_msgs
    plansys2_msgs
    plansys2_executor
    plansys2_domain_expert
    plansys2_problem_expert
    plansys2_planner
    plansys2_pddl_parser
    plansys2_bt_actions
    ament_index_cpp
)

# use header files from include directory
include_directories(include)

# create shared library targets from bt nodes
add_library(navigate_bt_node SHARED src/bt_nodes/Navigate.cpp)
list(APPEND plugin_libs navigate_bt_node)

add_library(approach_pallet_bt_node SHARED src/bt_nodes/ApproachPallet.cpp)
list(APPEND plugin_libs approach_pallet_bt_node)

add_library(recharge_bt_node SHARED src/bt_nodes/Recharge.cpp)
list(APPEND plugin_libs recharge_bt_node)

add_library(lift_fork_bt_node SHARED src/bt_nodes/LiftFork.cpp)
list(APPEND plugin_libs lift_fork_bt_node)

add_library(lower_fork_bt_node SHARED src/bt_nodes/LowerFork.cpp)
list(APPEND plugin_libs lower_fork_bt_node)

foreach(bt_plugin ${plugin_libs})
  ament_target_dependencies(${bt_plugin} ${dependencies})
  target_compile_definitions(${bt_plugin} PRIVATE BT_PLUGIN_EXPORT)
endforeach()

add_executable(nav2_action_server_node src/nav2_action_server_node.cpp)
ament_target_dependencies(nav2_action_server_node ${dependencies})

# copy install directories to 
install(DIRECTORY bt_xml config launch pddl DESTINATION share/${PROJECT_NAME})

install(TARGETS
  nav2_action_server_node
  ${plugin_libs}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

ament_export_dependencies(${dependencies})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
