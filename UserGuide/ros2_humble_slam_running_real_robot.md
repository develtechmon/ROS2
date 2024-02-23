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
to ensure it's recognizable and work with our Lidar `base_frame` above.

Please check `Lidar` section at `core.robot.xacro` on how to setup this parameter.

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

## Step 4 : Build the directory again
From top directory run following command to compile all the changes that we made just now. 
```
colcon build
. install/setup.bash
```

## Step 5 : To start mapping, follow this sequence
```
## In new terminal run following 
ros2 launch techdiffbot launch_robot.launch.py

## In new terminal run following. Here we're using `ldlidar_link` as our Frame to ensure it matches with our URDF file
. install/setup.bash
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=ldlidar_link

## In new terminal run following command to start with the mapping
ros2 run slam_toolbox async_slam_toolbox_node src/techdiffbot/config/mapper_params_online_async.yaml 

## Open Rviz2
rviz2
select map
and choose map as map
```
