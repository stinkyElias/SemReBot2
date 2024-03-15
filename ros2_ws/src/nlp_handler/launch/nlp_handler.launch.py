import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
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
        output='screen',
        parameters=[
            os.path.join(this_directory, 'config', 'params.yaml')
        ]
    )

    mistral_cmd = Node(
        package='nlp_handler',
        executable='mistral_node',
        name='mistral_node',
        namespace=namespace,
        output='screen',
        parameters=[
            os.path.join(this_directory, 'config', 'params.yaml')
        ]
    )

    ld = LaunchDescription()

    ld.add_action(declare_namespace_cmd)
    ld.add_action(whisper_cmd)
    ld.add_action(mistral_cmd)

    return ld