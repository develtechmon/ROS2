# Getting Started

In this userguide, i'm going to show on how to runnig SLAM in our actual robot that made of
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
-    mode: mapping 
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
To ensure we're using `correct` lidar link, we have to modify 
