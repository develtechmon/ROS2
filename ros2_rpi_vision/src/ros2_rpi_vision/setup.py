from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'ros2_rpi_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    #packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'meshes'),glob('meshes/*')),
        (os.path.join('share', package_name, 'launch'),glob('launch/*')),
        (os.path.join('share', package_name, 'urdf'),glob('urdf/*'))
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
        ],
    },
)
