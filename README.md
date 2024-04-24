# ROS 2 Semantic Reasoning in Robots

## How to use

Terminal 1: ros2 launch semrebot2_bringup bringup.launch.py

Terminal 2: ros2 run semrebot2_task_controller nav2_sim_node

Terminal 3: ros2 run semrebot2_task_controller task_controller_node

Terminal 4: ros2 topic pub --once /speech std_msgs/msg/Int8 "{data: x}" -> where 1 <= x <= 4

### Important

The package semrebot2_natural_language_processer is dependent on the domain.pddl file in /package semrebot2_task_controller/pddl. Make sure the path to this file is correct on your system. Default is ~/ros2_ws/src/semrebot2/semrebot2_task_controller_node
