from setuptools import find_packages, setup

package_name = 'rpi_pc_talk'

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
            'publisher = rpi_pc_talk.publisher:main',
            'subscriber = rpi_pc_talk.subscriber:main'
        ],
    },
)
