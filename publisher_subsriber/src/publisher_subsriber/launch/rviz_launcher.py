from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    package_share_dir = get_package_share_directory("publisher_subsriber")
    urdf_file_path = os.path.join(package_share_dir, "urdf", "publisher_subscriber.urdf")
    return LaunchDescription([
        Node(
            package='rviz2',
            namespace='rviz2',
            executable='rviz2',
            name='simulation_in_rviz'
        ),
    ])