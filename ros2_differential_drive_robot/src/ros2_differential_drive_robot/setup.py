from setuptools import find_packages, setup
import os 
from glob import glob
package_name = 'ros2_differential_drive_robot'

setup(
    name=package_name,
    version='0.0.0',
    #packages=[package_name],
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'description'), glob('description/*'))

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
            'lidar_obstacle = ros2_differential_drive_robot.lidar_obstacle:main',
            'lidar_obstacle_steer = ros2_differential_drive_robot.lidar_obstacle_steer_leftright:main',
            'lidar_dynamic_obstacle = ros2_differential_drive_robot.lidar_dynamic_obstacle:main',
        ],
    },
)
