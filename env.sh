#!/bin/bash

source /opt/ros/rolling/setup.bash
export TURTLEBOT3_MODEL=waffle
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/rolling/share/turtlebot3_gazebo/models

source install/setup.bash
colcon build --symlink-install --packages-select task_controller nlp_handler
source install/setup.bash
