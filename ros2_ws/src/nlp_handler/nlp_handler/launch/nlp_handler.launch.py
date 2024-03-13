import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    this_directory = get_package_share_directory('nlp_handler')
    namespace = LaunchConfiguration('namespace')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace'
    )

    whisper_cmd = Node(
        package='nlp_handler',
        executable='whisper_node',
        name='whisper_node',
        namespace=namespace,
        output='screen'
    )