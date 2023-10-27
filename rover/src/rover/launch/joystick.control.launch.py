import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    # Declare a launch argument for the parameter value
    require_enable_button_arg = DeclareLaunchArgument(
        'require_enable_button',
        default_value='false',
        description='Set the require_enable_button parameter'
    )

    # Launch the 'teleop_twist_joy_node' with the parameter
    teleop_twist_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_twist_joy_node',
        name='teleop_twist_joy_node',
        output='screen',
        namespace='teleop_twist_joy_node',  # Specify the node's namespace
        parameters=[{'require_enable_button': DeclareLaunchArgument('require_enable_button')}]
    )

    return LaunchDescription([
        require_enable_button_arg,
        teleop_twist_joy_node
    ])
