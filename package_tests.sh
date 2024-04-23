#!/bin/bash

# take $i as a command line argument
i=$1

source install/setup.bash

# Start whisper, mistral, and plansys2 nodes
ros2 launch semrebot2_bringup bringup.launch.py &
sleep 2 # give some time for nodes to start

# Start task_controller_node in a new terminal
ros2 run semrebot2_task_controller task_controller_node &
sleep 40 # ensure it is fully started

# Publish a single Int8 message to /speech topic
ros2 topic pub --once /speech std_msgs/msg/Int8 "{data: $i}"

# Wait for the nodes to process the command
sleep 60 # adjust based on expected processing time

kill $!