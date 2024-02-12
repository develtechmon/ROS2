# Getting started

This command is used to launch our `Simulated` robot using `Gazebo` and `Rviz`.
Morever, this command will publish `robot_state_publisher`.

## To launch our `Full Script`
In this launch file, it will launch `Gazebo`, `Rviz`,`robot_state_publisher`, `spawner` at one. Which will be needed for our `Gazebo World`. You can refer to separate command as shown in other `Launcher` below. 
- ros2 launch src/ros2_differential_drive_robot/launch/gazebo.sim.launch.py

## To launch `Robot` in `Gazebo`
- ros2 launch gazebo_ros gazebo.launch.py

## To launch `Robot` in `Rviz2`
- rviz2

Alternatively, you can use below command to launch `robot_state_publisher`,`joint_state_publisher_gui` and `rviz2`
- ros2 launch src/ros2_differential_drive_robot/launch/rviz2.launch.py 

## To launch `robot_state_publisher`
- ros2 launch src/ros2_differential_drive_robot/launch/rsp.launch.py use_sim_time:=true

## To launch `robot_state_publisher gui` to control our `wheel`
- ros2 run joint_state_publisher_gui joint_state_publisher_gui

## To `spawn` our `Robot` into `Gazebo` world
- ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity lukebot

## To launch the `saved world` in Gazebo
- ros2 launch ros2_differential_drive_robot gazebo.sim.launch.py world:=/src/ros2_differential_drive_robot/worlds/obstacle_avoidance.world

## To launch the `saved world` in Gazebo directly using Gazebo command directly
- ros2 launch gazebo_ros gazebo.launch.py world:=./src/techdiffbot/world/gazebo_techdiffbot_first_world

## To launch and view our `saved rviz2` file
- rviz2 -d src/articubot_one/config/view_bot.rviz

## To launch and view our `saved Gazebo` file in a `Gazebo` with `rviz`, `robot_state_publisher` and `spawner`
- ros2 launch mybot gazebo.sim.launch.py world:=./src/articubot_one/worlds/obstacles.world

## To listen to `lidar frame` topic `/scan`
- ros2 topic echo /scan 

## To run our `keyboard` control
- ros2 run teleop_twist_keyboard teleop_twist_keyboard

## To re-map velocity topic
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
