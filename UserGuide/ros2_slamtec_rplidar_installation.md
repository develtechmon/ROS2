# Getting Started

This is userguide on how to install `Slamtec C1 lidar` ROS2 package.

## Step 1 : Create Directory and Build The Package

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

## Step 3 : Create Udev for our Lidar

rplidar_ros running requires the read and write permissions of the serial device. You can manually modify it with the following command:
```
sudo chmod 777 /dev/ttyUSB0
```

But a better way is to create udev rule:
```
cd src/rplidar_ros
source scripts/create_udev_rules.sh
```

You can see now, we  have assigned the port. You can run following command to see the output
```
ls -l /dev | grep ttyUSB
```

Output as follow. Our new port is named as `/dev/rplidar` instead of `ttyUSB0`
```
lrwxrwxrwx  1 root   root           7 Oct 29 15:35 ldlidar -> ttyUSB0 (This one for ldlidar)
lrwxrwxrwx  1 root   root           7 Oct 29 15:35 rplidar -> ttyUSB0 (This one for slamtec)
crwxrwxrwx  1 root   dialout 188,   0 Oct 29 15:35 ttyUSB0
```

## Step 2 : Run our Lidar

To run the lidar, we will use these 2 methods

* Using Launch
```
ros2 launch rplidar_ros rplidar_c1_launch.py
```
Then open your `rviz2` and set the following
```
Fixed Frame : laser
LaserScan : Topic : /scan
```

* Using Run, but here we pass `/dev/rplidar` as a serial_port
```
ros2 run rplidar_ros rplidar_node --ros-args -p serial_port:=/dev/rplidar -p serial_baudrate:=460800 -p frame_id:=ldlidar_link
```

Then open your `rviz2` and set the following
```
Fixed Frame : ldlidar_link
LaserScan : Topic : /scan
```
