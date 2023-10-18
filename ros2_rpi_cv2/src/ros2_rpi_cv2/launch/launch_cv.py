from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # Launch the camera_publisher node
        Node(
            package='ros2_rpi_cv2',
            executable='camera_publisher',
            name='camera_publisher',
            output='screen',
        ),

        # Launch the camera_mp_handdetection_subscriber node
        Node(
            package='ros2_rpi_cv2',
            executable='camera_mp_handdetection_subscriber',
            name='camera_mp_handdetection_subscriber',
            output='screen',
        ),

        # Launch the camera_subscriber_mp_posedetection node
        Node(
            package='ros2_rpi_cv2',
            executable='camera_mp_posedetection_subscriber',
            name='camera_mp_posedetection_subscriber',
            output='screen',
        ),

        # Launch the camera_mp_facedetection_subscriber node
        Node(
            package='ros2_rpi_cv2',
            executable='camera_mp_facedetection_subscriber',
            name='camera_mp_facedetection_subscriber',
            output='screen',
        ),
    ])
