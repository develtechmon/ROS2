# Getting Started

This is separate userguide from `ros2_humble_slam_simulation_and_realrobot_guide_using_slamtec_lidar.md`
that aim for `simulation` only. I think it's very important to have a separate userguide that explain step by step
guide on how to run `SLAM` and `nav2` properly for better clarity.

## Step 1: Install `ros2` packages

In your development `Laptop`, `Desktop` with `ros2` and `Ubuntu 22` install following package first to ensure we can run the simulation and even real robot properly.

```
sudo apt-get install tree
sudo apt-get install ros-humble-xacro
sudo apt install ros-humble-joint-state-publisher-gui
sudo apt-get install ros-humble-teleop-twist-keyboard
sudo apt-get install ros-humble-teleop-twist-joy
sudo apt-get install ros-humble-gazebo-ros-pkgs 
sudo apt-get install joystick jstest-gtk evtest
sudo apt install ros-humble-joy-tester
sudo apt-get install v4l-utils
sudo apt-get install ros-humble-twist-mux

sudo apt-get install v4l-utils ros-humble-v4l2-camera
sudo apt-get install ros-humble-image-transport-plugins ros-humble-rqt-image-view
sudo apt-get install ros-humble-rqt-image-view

sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros2-control
sudo apt install ros-humble-controller-manager

sudo apt-get install ros-humble-cv-bridge
sudo apt install ros-humble-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp <--- Later include this in your /.bashrc file later

sudo apt-get install ros-humble-slam-toolbox

sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*
sudo apt-get install ros-humble-nav2*
sudo apt-get install ros-humble-tf2*

sudo apt-get install python3-serial
sudo apt install python3-pip
```

## Step 2: Clone our `techdiffbot` package and build

In your development `pc`, open new terminal and git clone following package from my `github page`

```
git clone https://github.com/develtechmon/ROS2.git
```
Then build the packages as follow
```
cd /home/jlukas/Desktop/My_Project/ROS2/techdiffbot
rm -rf build install log <--- To remove previously build packages for clean build in our new run later
```
Acquire the package and resolve depedencies using below command
```
rosdep update && rosdep install --from-path src --ignore-src -y
```
Build and source the packages
```
colcon build --symlink-install
. install/setup.sh
```

## Step 3: Change Wheel Position

I find this is quite strange because right wheels and left wheel motor didn't match similarly as simulation.
To solve this, i swap left and right wheel the parameters in `my_controllers.yaml` file.

Open the `yaml` file below 
```
src/techdiffbot/config/my_controllers.yaml
```

And change the `wheel position` as follow for `simulation`
```
base_frame_id: base_link

right_wheel_names: ['reft_wheel_joint']
left_wheel_names: ['light_wheel_joint']
wheel_separation: 0.21
wheel_radius: 0.03405
```

## Step 3 : SLAM setup for Simulation

To start with `mapping` please enable `mode:mapping` inside `mapper_params_online_async.yaml` file as follow.
Here we're enabling `mapping mode` to start.

open the `yaml` file
```
vi src/techdiffbot/config/mapper_params_online_async.yaml 
```

and Enable `mapping` mode as follow.
```
# ROS Parameters
odom_frame: odom
map_frame: map
#base_frame: ldlidar_base
base_frame: base_footprint 
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
mode: mapping <---- Please enable this line to start mapping

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
#mode: localization
```
Then save and quit.


## Step 4: Start Mapping in simulation

```
1. In new terminal run Gazebo
ros2 launch techdiffbot gazebo.sim.launch.py  world:=./src/techdiffbot/world/my_maze 

2. In new terminal run Rviz
rviz2 -d src/techdiffbot/rviz2/my_maze.rviz 

3. In new terminal run SLAM toolbox
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

Above command is similar to below command. What make it different, is that one using launcher and other is run
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

4. From Rviz select
   Fixed Frame - map
   Map Topic - Map

5. In new terminal run Joystick or Keyboard control start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

Move the robot around the area and once you're done please return the robot to its original initial
position in map at which point it start to move. Then save the gazebo map into your /config/world/

## 




