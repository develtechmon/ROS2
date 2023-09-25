from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'publisher_subsriber'

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
            'publishers_node = publisher_subsriber.publisher_node:main',
            'subscribers_node = publisher_subsriber.subscriber_node:main',
        ],
    },
)
