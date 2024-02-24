# Getting Started

In this userguide, i'm going to show on how to running SLAM in our actual robot that made of
* LD019 Lidar x 1
* RPi 4B 4GB x 1
* 2 Encoder Motor x 2
* Arduino Nano x 1
* Motor Driver L298N x 1
* 11V 5500mAH battery

## Step 1 : Go to `techdiffbot` directory
From this directory we need to modify followng file

Open this `src/techdiffbot/config/mapper_params_online_async.yaml` file and modify following
parameters to ensure it match to our Lidar Transform 
```
     # ROS Parameters
     odom_frame: odom
     map_frame: map
     base_frame: ldlidar_base <---- This is our ldlidar_base that match to our Lidar URDF Link that hold the Lidar
     #base_frame: base_footprint
     #scan_topic: /ldlidar_node/scan
     scan_topic: /scan
     use_map_saver: true
 
     # 1: To start with mapping - enable mapping mode below
     mode: mapping 
```

## Step 2 : Change Wheel Position
I find this is quite strange because `right wheels` and `left wheel motor` didn't match similarly as simulation. 
To solve this, i swap left and right `wheel` the parameters in `src/techdiffbot/config/my_controllers.yaml`

```
base_frame_id: base_link

right_wheel_names: ['left_wheel_joint']
left_wheel_names: ['right_wheel_joint']
wheel_separation: 0.21
wheel_radius: 0.03405
 
```

## Step 3 : Change `src/techdiffbot/urdf/core.robot.xacro` file parameter
To ensure we're using `correct` lidar link, we have to modify `link` and `joint name` parameter under `Lidar` section
to ensure it's recognizable and work with our `ldlidar_base` and `ldlidar_link` above.

Please check `Lidar` section at `core.robot.xacro` on how to setup this parameter. Below example i'm using an example of
Lidar from `articubot` to make things easy to understand.
```
    <joint name="laser_joint" type="fixed">
        <parent link="chassis"/>
        <child link="ldlidar_base"/> 
        <origin xyz="0.122 0 0.212" rpy="0 0 0"/>
    </joint>

    <link name="ldlidar_base"> <================================= our ldlidar_base
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.04"/>
            </geometry>
            <material name="black"/>
        </visual>
        <visual>
            <origin xyz="0 0 -0.05"/>
            <geometry>
                <cylinder radius="0.01" length="0.1"/>
            </geometry>
            <material name="black"/>
        </visual>
        <collision>
            <geometry>
                <cylinder radius="0.05" length="0.04"/>
            </geometry>
        </collision>
        <xacro:inertial_cylinder mass="0.1" length="0.04" radius="0.05">
            <origin xyz="0 0 0" rpy="0 0 0"/>
        </xacro:inertial_cylinder>
   </link>

    <joint name="ldlidar_link_joint" type="fixed">
        <parent link="ldlidar_base"/>
        <child link="ldlidar_link"/>
        <origin xyz="0 0 0.02745" rpy="0 0 0" />
    </joint>

    <link name="ldlidar_link"> <================================= our ldlidar_link
        <visual>
            <geometry>
                <cylinder radius="0.05" length="0.04"/>
            </geometry>
            <material name="black"/>
        </visual>
        <visual>
            <origin xyz="0 0 -0.05"/>
            <geometry>
                <cylinder radius="0.01" length="0.1"/>
            </geometry>
            <material name="black"/>
        </visual>
        <collision>
            <geometry>
                <cylinder radius="0.05" length="0.04"/>
            </geometry>
        </collision>
        <xacro:inertial_cylinder mass="0.1" length="0.04" radius="0.05">
            <origin xyz="0 0 0" rpy="0 0 0"/>
        </xacro:inertial_cylinder>
   </link>

```

## Step 3 : Set fixed `bus ID` to our Arduino port.
See below example on how I set a fixed port ID for arduino nano which is configure inside `src/techdiffbot/urdf/ros2_control.xacro`
```
       <param name="left_wheel_name">left_wheel_joint</param>
       <param name="right_wheel_name">right_wheel_joint</param>
       <param name="loop_rate">30</param>
       <param name="device">/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0</param> <------- set the Port numbe by constant path
       <param name="baud_rate">57600</param>
       <param name="timeout_ms">1000</param>
       <param name="enc_counts_per_rev">1320</param>
```

## Step 4 : To start mapping, enable followig mode 

To start with `mapping` please enable `mode:mapping` inside `mapper_params_online_async.yaml` file as follow Here we're using mapping mode to start
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: ldlidar_base <---- This is our ldlidar_base that match to our Lidar URDF Link that hold the Lidar
scan_topic: /scan
use_map_saver: true
mode: mapping <--------------Enable this
```

From top directory run following command to compile all the changes that we've made just now. 
```
colcon build
. install/setup.bash
```

## Step 6 : To start with mapping of our environment

Follow below command by sequence.
```
## In new terminal run following
. install/setup.bash
ros2 launch techdiffbot launch_robot.launch.py

## In new terminal run following. Here we're using `ldlidar_link` as our lidar_frame to ensure it matches with our URDF file
. install/setup.bash
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=ldlidar_link

## In new terminal run following command to start with the mapping
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml 

## Might consider to run this commad to have a static transform - optional
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 odom ldlidar_base

## Open Rviz2
rviz2
select map
and choose map as map

## ros2 run techdiffbot to use our Steam controller to move the robot
ros2 launch techdiffbot joystick.control.launch.py 

```

## Step 7 : To start navigation, enable followig mode 
To start with `navigation` please enable `mode:localization` and disable `mode: mapping` inside `mapper_params_online_async.yaml` file.
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: ldlidar_base <---- This is our ldlidar_base that match to our Lidar URDF Link that hold the Lidar
#base_frame: base_footprint
#scan_topic: /ldlidar_node/scan
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
#mode: mapping <--------------Disable this

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
mode: localization <--------------Enable this

map_file_name: /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/my_maze_serial
map_start_at_dock: true
#map_start_pose: [0.0, 0.0, 0.0]
```

From top directory run following command to compile all the changes that we've made just now. 
```
colcon build
. install/setup.bash
```

## Step 8 : To start with navigation of our environment

Follow below command by sequence.
```
## In new terminal run following
. install/setup.bash
ros2 launch techdiffbot launch_robot.launch.py

## In new terminal run following. Here we're using `ldlidar_link` as our lidar_frame to ensure it matches with our URDF file
. install/setup.bash
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=ldlidar_link

## In new terminal run following command to start with the navigation
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

This command is similar to below command:
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

## Run below command to bringup the Navigation
ros2 launch nav2_bringup navigation_launch.py use_sime_time:=false -- For top

## Run below command to bringup the Navigation if you already copy the `navigatio_launc.py` and `nav2_params.yaml` file and edit the configuration. Then run this command
ros2 launch techdiffbot navigation_launch.py use_sim_time:=true

## Might consider to run this commad to have a static transform - optional
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 odom ldlidar_base

## Open Rviz2
rviz2
select map
and choose map as map

From map --> Select Topic --> global../costmap
color scheme --> costmap


And then pres 2D Goal pose to start navigation
```
