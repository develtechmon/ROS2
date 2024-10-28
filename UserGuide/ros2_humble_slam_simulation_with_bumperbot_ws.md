# Getting Started

Package details as follow
* My Package name : bumperbot_ws
* ROS2 Humble
* Tested and run in Ubuntu
```
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.5 LTS
Release:	22.04
Codename:	jammy
```

## For Simulation inside PC

This is userguide on how to to run `SLAM` using `SLAM Graph`. Please follow the following

## Step 1 : Go to right directory

Please follow this userguide
```
cd bumperbot_ws
```

## Step 2 : Run Simulation

Open terminal run the `robot simulation` file as follow. Here we're launching robot description, controller, gazebo, joystick.
```
ros2 launch bumperbot_bringup gazebo.sim.launch.py
```

## Step 3 : Run SLAM

Open new terminal and run below command. Here we specify `use_sim_time:=true` for simulation
```
ros2 launch bumperbot_bringup slam.launch.py use_sim_time:=true
```

## Step 4 : Open Rviz

Open new terminal and please follow below step
```
rviz2
```

Please apply `rviz2` settings as follow
```
Fixed Frame - map
LaserScan - Topic - /scan
RobotMode - Description Topic - /robot_description
Map - Topic - /map
```

At this point you should already see the `SLAM` map  from layout.

## Step 5 : Control The Robot

You can either use `Steam Joystick` to move the robot to start mapping.

Or use below command to control the robot using keyboard in new terminal
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap /cmd_vel:=/diff_cont/cmd_vel_unstamped
```
