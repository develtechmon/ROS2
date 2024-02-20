PIXHAWK Pro
- > using JST GH port
- > GH1.25 port

PIXHAWK 2.4.8
- > using Molex Picoblade
- > JST 1.25mm
- > CH1.25 port


## Install the nav2 package
sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*
sudo apt-get install ros-humble-nav2*
sudo apt-get install ros-humble-turtlebot3*
sudo apt-get install ros-humble-navigation2
sudo apt-get install ros-humble-nav2-bringup
sudo apt-get install ros-humble-tf2*

## Launch gazebo_simulation_file with our slam_world
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/slam_world
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/gazebo_techdiffbot_first_world 

## To create map and saved our map. (after mapping, this function can be executed)

For Foxy
ros2 launch slam_toolbox online_async_launch.py params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true 

For Humble
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

rviz2


In "mapper_params_online_async.yaml" file please ensure those param is enabled for mapping:
# 1: To start with mapping - enable mapping mode below
mode: mapping <---------
	
Use rviz2 settings follow:
1. add Map
2. Topic - /map
3. Update Topic - /map_updates
4. Global Options --> Fixed Frame - map
5. LaserScan --> Topic - /scan
             --> depth - 6
			 --> History Policy - Keep Last
			 --> Reliability Policy - Best Effort
			 --> Durability Policy - Volatile

Run keyboard control command below to move our robot and start mapping
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

From "rviz2" select add_panel and select "SlamToolboxPlugin".
From there enter following details
1. Save map - new_slam_map
2. Serialize map - new_slam_serial_map

Click "serialize map"  button
Click "save map" button 

or run below command to save the map
ros2 run nav2_map_server map_saver_cli -f map/maze ---> to save map

at working directory in this case is "techdiffbot" you should see multiple files has been created as follow:
1. new_slam_map.pgm
2. new_slam_map.yaml
3. new_slam_serial_map.data
4. new_slam_serial_map.posegraph

Then again In "mapper_params_online_async.yaml" file please ensure those param is disabled and enabled for localization:
# 1: To start with mapping - enable mapping mode below
#mode: mapping <---- disable this because we're no doing mapping

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
mode: localization
map_file_name: /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/new_slam_serial <--- point this path to our saved map file
map_start_at_dock: true

Then run "colcon build" command and run below command to launch our gazebo simulation
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/new_slam_map 
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

## In other terminal source the "./install/bash" file. To bring up the saved map into our rviz2 please follow below sequence:
open "rviz2" first and follow below command sequence
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=my_map.yaml -p use_sim_time:=true
ros2 run nav2_util lifecycle_bringup map_server

At this point, you should the saved "map" in our "rviz2"

## Run our mcl model
ros2 run nav2_amcl amcl --ros-args -p use_sim_true:=true
ros2 run nav2_util lifecycle_bringup amcl

and select "2D pose estimate" to find best initial position in our "rviz2".
you may need to move the robot somwhere in the gazebo to find best location.

Remember:
To launch in our real robot use following command. In rpi4 machine
ros2 launch techdiffbot launch_robot.launch.py 

After that in our dev machine, we should see "odom" in Rviz2
And next we're going to run "lidar" command
ros2 launch techdiffbot lidar.launch.py

In rviz2 add map and use map topic

Next run below command to start mapping. Please enable "mode : mapping"
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=false

Next we're going to install "mux" package which can be used to select the priority of the function
sudo apt-get install ros-foxy-twist-mux

ros2 launch nav2_bringup navigation_launch.py use_sime_time:=true
from "rviz2" select Map --> Topic --> "/global_costmap/costmap
color Scheme --> costmap
