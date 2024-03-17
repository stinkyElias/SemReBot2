#!/bin/bash

source /opt/ros/rolling/setup.bash
export TURTLEBOT3_MODEL=waffle
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/rolling/share/turtlebot3_gazebo/models

source install/setup.bash
colcon build --symlink-install --packages-select semrebot2_task_controller semrebot2_natural_language_processer semrebot2_lifecycle_manager semrebot2_bringup
source install/setup.bash
