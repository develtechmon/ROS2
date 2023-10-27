import launch
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from time import sleep
def generate_launch_description():
    
    return LaunchDescription([

        #Set the parameter using ExecuteProcess
        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/teleop_twist_joy_node','require_enable_button', 'false'],
            output='screen',
        ),
        # Launch the 'teleop-twist-joy' using ExecuteProcess
        ExecuteProcess(
            cmd=['ros2', 'launch', 'teleop_twist_joy', 'teleop-launch.py'],
            output='screen',
        ),

    ])
