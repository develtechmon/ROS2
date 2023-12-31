from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ros2_rpi_lidar'

setup(
    name=package_name,
    version='0.0.0',
    # packages=find_packages(exclude=['test']),
    packages=[package_name],
    
    py_modules=[
        'ros2_rpi_lidar.distance',  # Add your module here
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'module'),glob('module/*')),

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
            'lidar_publisher  = ros2_rpi_lidar.lidar_publisher:main',
            'lidar_subscriber = ros2_rpi_lidar.lidar_subscriber:main',
            'lidar_publisher_rate = ros2_rpi_lidar.lidar_publisher_with_rate:main',
        ],
    },
)
