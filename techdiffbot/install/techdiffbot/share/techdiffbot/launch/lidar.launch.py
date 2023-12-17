from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ldlidar',
            executable='ldlidar',
            name='ldlidar_node',
            parameters=[
                {'lidar_frame': 'lidar_link'},
                {'serial_port': '/dev/ttyUSB1'}
            ]
        )
    ])

