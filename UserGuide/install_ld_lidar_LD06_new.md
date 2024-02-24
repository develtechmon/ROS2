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

To launch with specific port and lidar_link from urdf
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=lidar_link serial_port:=/dev/ttyUSB1

```

## Step 3: Launch our Package to work with `SLAM` in RViz2 based on `techdiffbot`

Run by sequence
```
1. ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/slam_toolbox.yaml use_sim_time:=false
2. ros2 launch ldlidar ldlidar.launch.py lidar_frame:=ldlidar_link
3. ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 odom base_footprint
4. ros2 launch techdiffbot launch_robot.launch.py
```
