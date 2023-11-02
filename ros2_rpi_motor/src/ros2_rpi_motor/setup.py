from setuptools import find_packages, setup

package_name = 'ros2_rpi_motor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jlukas',
    maintainer_email='jlukas@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'subscriber_node = ros2_rpi_motor.subscriber:main',
        'publisher_node = ros2_rpi_motor.publisher:main',
        'motor_subscriber_node  = ros2_rpi_motor.motor_subscriber:main',
        'motor_l298n = ros2_rpi_motor.motor_l298n:main',
        ],
    },
)
