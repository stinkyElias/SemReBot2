cmake_minimum_required(VERSION 3.8)
project(semrebot2_lifecycle_manager)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(lifecycle_msgs REQUIRED)

set(dependencies
  rclcpp
  rclcpp_lifecycle
  lifecycle_msgs
)

include_directories(include)

add_library(${PROJECT_NAME}
  src/LifecycleManager.cpp
)
ament_target_dependencies(${PROJECT_NAME} ${dependencies})

add_executable(lifecycle_manager_node
  src/lifecycle_manager_node.cpp
)
ament_target_dependencies(lifecycle_manager_node ${dependencies})
target_link_libraries(lifecycle_manager_node ${PROJECT_NAME})

install(DIRECTORY include/
  DESTINATION include
)

install(TARGETS
  ${PROJECT_NAME}
  lifecycle_manager_node
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

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

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(${dependencies})

ament_package()
