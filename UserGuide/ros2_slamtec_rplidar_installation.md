# Getting Started

This is userguide on how to install `Slamtec C1 lidar` ROS2 package.

## Step 1 : Create Directory

Plesae follow this step either in your`RPI` or `PC`
```
cd ~
mkdir -p lidar_slamtec/src
cd lidar_slamtec/src
```

Inside `src`, please clone this package which is for `ros2`. Here, we checkout for `ros2` specific
```
git clone https://github.com/Slamtec/rplidar_ros2.git -b ros2
```

Then build the package
```
cd ~lidar_slamtec
colcon build --symlink-install

source ./install/setup.bash
```

upon successfull build, you can consider to add this package into bashrc script
```
echo source $(pwd)/install/local_setup.bash >> ~/.bashrc
source ~jlukas/.bashrc
```
