## Getting Started 

In this guide we're going to install update new `LD06` lidar to our `machine`. This is another revision from
the original repository.

## Step 1: Link
Refer to this link to get started
```
https://github.com/linorobot/ldlidar/tree/ros2
```

## Step 2: Git clone packages to our working directory as follow
```
mkdir ldlidar_ros2_ws_new
cd ldlidar_ros2_ws_new
mkdir src
cd src
git clone https://github.com/linorobot/ldlidar.git ldlidar
cd ..
sudo rosdep init
rosdep update && rosdep install --from-path src --ignore-src -y

colcon build

```

## Step 3: Launch our Package to work with `Odom` in RViz2
```
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=odom

To launch with specific port:
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=odom serial_port:=/dev/ttyUSB1
```
