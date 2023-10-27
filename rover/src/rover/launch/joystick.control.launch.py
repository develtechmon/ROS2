import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Declare a launch argument for the parameter value
        DeclareLaunchArgument(
            'require_enable_button',
            default_value='false',
            description='Set the require_enable_button parameter'
        ),
        # Launch the 'teleop_twist_joy_node' and set the parameter
        Node(
            package='teleop_twist_joy',
            executable='teleop_twist_joy_node',
            name='teleop_twist_joy_node',
            namespace='',
            output='screen',
            parameters=[{'require_enable_button': LaunchConfiguration('require_enable_button')}]
        )
    ])
