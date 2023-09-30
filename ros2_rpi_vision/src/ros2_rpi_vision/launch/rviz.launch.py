from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro
import os


def generate_launch_description():
    package_name = 'ros2_rpi_vision'

    rsp = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory(package_name),'launch','rsp.launch.py'
            )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    return LaunchDescription([    
                              
        rsp,

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='jst_gui'
        ),
        
        Node(
            package='rviz2',
            namespace='rviz2',
            executable='rviz2',
            name='simulation_in_rviz2'
        ),
        
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
    ])
