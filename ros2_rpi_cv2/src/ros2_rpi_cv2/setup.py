from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ros2_rpi_cv2'

setup(
    name=package_name,
    version='0.0.0',
    #packages=find_packages(exclude=['test']),
    packages=[package_name],

    # py_modules=[
    #     'ros2_rpi_cv2.cv2_vision', # Add your scripts module here
    # ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jlukas',
    maintainer_email='lukasjohnnytechmon@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_publisher = ros2_rpi_cv2.camera_publisher:main',
            'camera_subscriber = ros2_rpi_cv2.camera_subscriber:main',
            'camera_publisher_no_timer = ros2_rpi_cv2.camera_publisher_no_timer:main',
            'camera_mp_facedetection_subscriber = ros2_rpi_cv2.camera_subscriber_mp_facedetection:main',
            'camera_mp_posedetection_subscriber = ros2_rpi_cv2.camera_subscriber_mp_posedetection:main',
            'camera_mp_handdetection_subscriber = ros2_rpi_cv2.camera_subscriber_mp_handdetection:main',
        ],
    },
)
