import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    parent_dir = '/home/stinky/ros2_ws/src/semrebot2'
    namespace = LaunchConfiguration('namespace')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace')

    semrebot2_task_controller_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            parent_dir,
            'semrebot2_task_controller/launch',
            'task_controller.launch.py')),
        launch_arguments={
            'namespace': namespace,
        }.items()
    )

    semrebot2_nlp_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            parent_dir,
            'semrebot2_natural_language_processer/launch',
            'natural_language_processer.launch.py')),
        launch_arguments={
            'namespace': namespace,
        }.items()
    )

    semrebot2_lifecycle_mngr_cmd = Node(
        package='semrebot2_lifecycle_manager',
        executable='lifecycle_manager_node',
        namespace=namespace,
        output='screen',
    )
    
    ld = LaunchDescription()

    ld.add_action(declare_namespace_cmd)
    ld.add_action(semrebot2_task_controller_cmd)
    ld.add_action(semrebot2_lifecycle_mngr_cmd)
    ld.add_action(semrebot2_nlp_cmd)

    return ld