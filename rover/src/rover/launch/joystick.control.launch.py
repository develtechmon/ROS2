import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, ExecuteProcess
from launch.conditions import UnlessLaunchConfiguration
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Launch the 'teleop-twist-joy' node with 'teleop-launch.py'
        ExecuteProcess(
            cmd=['ros2', 'launch', 'teleop_twist_joy', 'teleop-launch.py'],
            output='screen',
            name='teleop_twist_joy_launch',
        ),
        # Add a brief delay before setting the parameter (adjust as needed)
        LogInfo(
            condition=launch.conditions.LaunchConfiguration('verbose'),
            value='Waiting for a moment before setting the parameter...',
        ),
        # Set the 'require_enable_button' parameter to 'false'
        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/teleop_twist_joy_node/require_enable_button', 'false'],
            output='screen',
            name='set_param',
        ),
        DeclareLaunchArgument(
            'verbose',
            default_value='false',
            description='Enable verbose output'
        ),
        # You can adjust the sleep duration to suit your needs
        ExecuteProcess(
            cmd=['sleep', '2'],
            output='screen',
            name='wait_before_setting_param',
            condition=UnlessLaunchConfiguration('verbose'),
        ),
    ])


# import launch
# from launch import LaunchDescription
# from launch.actions import ExecuteProcess

# def generate_launch_description():
#     return LaunchDescription([
#         # Launch the 'teleop-twist-joy' using ExecuteProcess
#         ExecuteProcess(
#             cmd=['ros2', 'launch', 'teleop_twist_joy', 'teleop-launch.py'],
#             output='screen',
#         ),
#         # Set the parameter using ExecuteProcess
#         ExecuteProcess(
#             cmd=['ros2', 'param', 'set', '/teleop_twist_joy_node/require_enable_button', 'false'],
#             output='screen',
#         ),
#     ])
