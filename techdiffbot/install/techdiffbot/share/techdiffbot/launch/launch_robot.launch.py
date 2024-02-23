from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart, OnExecutionComplete
import os

def generate_launch_description():
    package_name = 'techdiffbot'

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','my_controllers.yaml')

    rsp = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory(package_name),'launch','rsp.launch.py'
            )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )
    
    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params],
            remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
        )

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description},
                    controller_params_file],
    )
    
    delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])
    
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    # Original - Using OnProcessStart
    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    # # Revise  - Using OnExecutionComplete
    # delayed_diff_drive_spawner = RegisterEventHandler(
    #     event_handler=OnExecutionComplete(
    #         target_action=controller_manager,
    #         on_start=[diff_drive_spawner],
    #     )
    # )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    '''
    Here, join_broad_spawner will be started after controller_manager finished its execution.
    This is also similar to below code:

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnExecutionComplete(
            target_action=controller_manager,
            on_completion=[joint_broad_spawner],
        )
    )

    See this link: https://roboticscasual.com/tutorial-ros2-launch-files-all-you-need-to-know/
    '''

    # Original - Using OnProcessStart
    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    # Revise  - Using OnExecutionComplete
    # delayed_joint_broad_spawner = RegisterEventHandler(
    #     event_handler=OnExecutionComplete(
    #         target_action=controller_manager,
    #         on_completion=[joint_broad_spawner],
    #     )
    # )
    
    joystick = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory(package_name),'launch','joystick.control.launch.py'
            )])
    )

    return LaunchDescription([    
        rsp,
        twist_mux,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner,
        #joystick,
        #rviz,
    ])
