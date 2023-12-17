from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'image_size',
            default_value='[640,480]',
            description='Size of the image'
        ),
        DeclareLaunchArgument(
            'camera_frame_id',
            default_value='camera_link_optical',
            description='Frame ID of the camera'
        ),
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='v4l2_camera_node',
            parameters=[
                {'image_size': LaunchConfiguration('image_size')},
                {'camera_frame_id': LaunchConfiguration('camera_frame_id')}
            ]
        )
    ])

