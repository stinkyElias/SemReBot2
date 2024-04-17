import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    this_directory = get_package_share_directory('semrebot2_task_controller')
    namespace = LaunchConfiguration('namespace')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Namespace'
    )

    plansys2_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            '/home/stinky/ros2_ws/src/plansys2/plansys2_bringup/launch',
            'plansys2_bringup_launch_monolithic.py')),
        launch_arguments={
            'model_file': os.path.join(this_directory, 'pddl', 'domain.pddl'),
            'namespace': namespace
        }.items()
    )

    # set actions
    # pass params and BT node to the action node
    navigate_cmd = Node(
        package='plansys2_bt_actions',
        executable='bt_action_node',
        name='navigate',
        namespace=namespace,
        output='screen',
        parameters=[
            os.path.join(this_directory, 'config', 'params.yaml'),
            {
                'action_name': 'navigate',
                'publisher_port': 1668,
                'server_port': 1669,
                'bt_xml_file': os.path.join(this_directory, 'bt_xml', 'navigate.xml')
            }
        ]
    )
    
    recharge_cmd = Node(
        package='plansys2_bt_actions',
        executable='bt_action_node',
        name='recharge',
        namespace=namespace,
        output='screen',
        parameters=[
            os.path.join(this_directory, 'config', 'params.yaml'),
            {
                'action_name': 'recharge',
                'bt_xml_file': os.path.join(this_directory, 'bt_xml', 'recharge.xml')
            }
        ]
    )
    
    transport_cmd = Node(
        package='plansys2_bt_actions',
        executable='bt_action_node',
        name='transport',
        namespace=namespace,
        output='screen',
        parameters=[
            os.path.join(this_directory, 'config', 'params.yaml'),
            {
                'action_name': 'transport',
                'publisher_port': 1670,
                'server_port': 1671,
                'bt_xml_file': os.path.join(this_directory, 'bt_xml', 'transport.xml')
            }
        ]
    )

    task_controller_cmd = Node(
        package='semrebot2_task_controller',
        executable='task_controller_node',
        name='task_controller',
        namespace=namespace,
        output='screen',
    )

    nav_cmd = Node(
        package='semrebot2_task_controller',
        executable='nav2_sim_node',
        name='nav2',
        namespace=namespace,
        output='screen',
    )

    ld = LaunchDescription()

    ld.add_action(declare_namespace_cmd)
    ld.add_action(plansys2_cmd)
    ld.add_action(navigate_cmd)
    ld.add_action(recharge_cmd)
    ld.add_action(transport_cmd)
    # ld.add_action(task_controller_cmd)
    ld.add_action(nav_cmd)

    return ld