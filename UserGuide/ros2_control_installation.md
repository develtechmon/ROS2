# Getting Started

This is userguide on how to install `ros2_control` that work for `Gazebo` and `Hardware`

## Step 1 : Install following libraries
```
sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros2-control
```

## Step 2 : To list down the list hardware interfaces

Please ensure that you have run `gazebo.sim.launch.py` or `launch_sim.launch.py` file first. From the log you see below log that indicate our controller manager in `Gazebo`
is running 
```
[INFO] [spawn_entity.py-4]: process has finished cleanly [pid 32072]
[gzserver-2] [INFO] [1699493278.897649746] [gazebo_ros2_control]: Loading joint: left_wheel_joint
[gzserver-2] [INFO] [1699493278.897728146] [gazebo_ros2_control]: 	State:
[gzserver-2] [INFO] [1699493278.897737546] [gazebo_ros2_control]: 		 velocity
[gzserver-2] [INFO] [1699493278.897745646] [gazebo_ros2_control]: 		 position
[gzserver-2] [INFO] [1699493278.897751846] [gazebo_ros2_control]: 	Command:
[gzserver-2] [INFO] [1699493278.898469347] [gazebo_ros2_control]: 		 velocity
[gzserver-2] [INFO] [1699493278.898511247] [gazebo_ros2_control]: Loading joint: right_wheel_joint
[gzserver-2] [INFO] [1699493278.898522147] [gazebo_ros2_control]: 	State:
[gzserver-2] [INFO] [1699493278.898530847] [gazebo_ros2_control]: 		 velocity
[gzserver-2] [INFO] [1699493278.898540047] [gazebo_ros2_control]: 		 position
[gzserver-2] [INFO] [1699493278.898548447] [gazebo_ros2_control]: 	Command:
[gzserver-2] [INFO] [1699493278.898560247] [gazebo_ros2_control]: 		 velocity
[gzserver-2] [INFO] [1699493278.898694747] [resource_manager]: Initialize hardware 'GazeboSystem' 
[gzserver-2] [INFO] [1699493278.898966347] [resource_manager]: Successful initialization of hardware 'GazeboSystem'
[gzserver-2] [INFO] [1699493278.899137047] [resource_manager]: 'configure' hardware 'GazeboSystem' 
[gzserver-2] [INFO] [1699493278.899154847] [resource_manager]: Successful 'configure' of hardware 'GazeboSystem'
[gzserver-2] [INFO] [1699493278.899162747] [resource_manager]: 'activate' hardware 'GazeboSystem' 
[gzserver-2] [INFO] [1699493278.899169847] [resource_manager]: Successful 'activate' of hardware 'GazeboSystem'
[gzserver-2] [INFO] [1699493278.899275447] [gazebo_ros2_control]: Loading controller_manager
[gzserver-2] [WARN] [1699493278.938636650] [gazebo_ros2_control]:  Desired controller update period (0.0333333 s) is slower than the gazebo simulation period (0.001 s).

```

In other terminal, run below command to see list of hardware interfaces
```
ros2 control list_hardware_interfaces
```

And you should below result indicate our `hardware` is found and `unclaimed`
```
command interfaces
	left_wheel_joint/velocity [available] [unclaimed]
	right_wheel_joint/velocity [available] [unclaimed]
state interfaces
	left_wheel_joint/position
	left_wheel_joint/velocity
	right_wheel_joint/position
	right_wheel_joint/velocity

```

## Step 3 : Spawn and run our controller Manager to configure `diff_cont`
```
ros2 run controller_manager spawner diff_cont
```
You will see below generated log
```
[INFO] [1699494487.156311218] [spawner_diff_cont]: Loaded diff_cont
[INFO] [1699494487.238620918] [spawner_diff_cont]: Configured and activated diff_cont
```

## Step 4 : Spawn and run our controller Manager to configure `joint_broad`
```
ros2 run controller_manager spawner joint_broad
```
You will see below generated log
```
[INFO] [1699494471.514335429] [spawner_joint_broad]: Loaded joint_broad
[INFO] [1699494471.566304330] [spawner_joint_broad]: Configured and activated joint_broad
```

## Step 5 : You're almost done. Next we're going to remap Velocity Control

Usually the `cmd_vel` is a common topic but not for `ros2_controller`. This controller
will publish new velocity topic as `/diff_cont/cmd_vel_unstamped`. Therefore we need to `remap` 
this topic to `cmd_vel`.

If you run below command
```
ros2 topic list
```

You will see below `available` list.
```
/camera/camera_info
/camera/image_raw
/clock
/diff_cont/cmd_vel_unstamped <-------
/diff_cont/odom
/diff_cont/transition_event
/dynamic_joint_states
/joint_broad/transition_event
/joint_states
/parameter_events
/performance_metrics
/robot_description
/rosout
/scan
/tf
/tf_static
```

To map our velocity map. Run below command
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

