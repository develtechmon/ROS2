import launch
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument,SetLaunchConfiguration
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
import os

def generate_launch_description():
    joystick = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('teleop_twist_joy'),'launch','teleop-launch.py'
            )]),
    launch_arguments={'cmd_vel_remapping': '/cmd_vel:=/diff_cont/cmd_vel_unstamped'}.items()

    )

    return LaunchDescription([
        joystick,

        ExecuteProcess(
         cmd=['ros2', 'param', 'set', '/teleop_twist_joy_node','require_enable_button', 'false'],
         output='screen',
         ),  
    ])

