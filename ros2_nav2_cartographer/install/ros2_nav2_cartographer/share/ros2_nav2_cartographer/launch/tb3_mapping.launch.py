from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    config_dir = os.path.join(get_package_share_directory('ros2_nav2_cartographer'),'config')
    return LaunchDescription([
        
        # Remember - To launch mapping. You can run turtlebo gazebo first, and then launch this file and lastly rviz
        Node(
            package='cartographer_ros',
            output='screen',
            executable='cartographer_node',
            name='cr_node',
            arguments=['-configuration_directory', config_dir,'-configuration_basename','turtlebot3_lds_2d.lua']
        ),
        Node(
            package='cartographer_ros',
            output='screen',
            executable='cartographer_occupancy_grid_node',
            name='cr_oc_node'
        ),

        # Node(
        # package='rviz2',
        # executable='rviz2',
        # name='rviz2',
        # #parameters=[{'use_sim_time': use_sim_time}],
        # output='screen'),

    ])