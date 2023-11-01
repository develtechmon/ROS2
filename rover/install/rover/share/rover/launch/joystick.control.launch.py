import launch
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from time import sleep
def generate_launch_description():
       
    set_param = ExecuteProcess(
        cmd=['ros2', 'param', 'set', '/teleop_twist_joy_node','require_enable_button', 'false'],
        output='screen',
    ),
    
    delay_execute_process = TimerAction(period=3.0, actions=[set_param])
    return LaunchDescription([

        #Set the parameter using ExecuteProcess
    
        # Launch the 'teleop-twist-joy' using ExecuteProcess
        ExecuteProcess(
            cmd=['ros2', 'launch', 'teleop_twist_joy', 'teleop-launch.py'],
            output='screen',
        ),


    ])

