## Getting Started

This userguide tell how to setup `SLAM` with ROS

## Step 1: Add `BASE_FOOTPRINT_LINK` into our `URDF` file
```
BASE LINK
<link name="base_link"></link>

BASE FOOTPRINT LINK
<joint name="base_footprint_joint" type="fixed">
<parent link="base_link"/>
<child link="base_footprint"/>
<origin xyz="0 0 0" rpy="0 0 0"/>

<link name="base_footprint"></link>
```
Our `base_link` is not actually on the ground but we can pretend it is and everythin will be OK. For this robot we are treating Z0 as the wheel axis.

## Step 2: Install the `Slam` and `Nav2` packages
```
sudo apt-get install ros-humble-twist-mux
sudo apt-get install ros-humble-slam-toolbox
sudo apt-get install ros-humble-nav2*
sudo apt-get install ros-humble-tf2*
sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*
```

Remember there are two type of such as `Online` and `Asynchronous`.
For `Online` - we are working on a live data stream rather than recorded logs

For `Asynchronous` - Always process the most recent scan to avoid lagging, even if that means skipping scans

## Step 3: Copy the `Yaml` file for `Slam` configuration
```
cp -r /opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/src/techdiffbot/config/

```

## Step 4: Edit the `Yaml` file with below Configuration

To start with `mapping` plese enable `mode:mapping` as follow
Here we're using `mapping` mode to start
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: base_footprint
scan_topic: /scan
use_map_saver: true
mode: mapping <--------------Enable this
```

## Step 5: Build our `Package`
```
colcon build 
source install/setup.bash
```

## Step 6: Launch `Gazebo world` with our `world` with following command
```
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/my_map 
```

## Step 7: Launch `rviz2 world` with following command
```
rviz2 -d src/techdiffbot/rviz2/my_map.rviz
```
or just launch normal rviz2 if you havent set any configuration yet
```
rviz2
```
At this point, no `map` topic post yet. You can add the following first for initial setup
```
Fixed Frame : odom
Robot Model :
     Description Topic : /robot_description
```

## Step 8: To start Mapping Launch our `Slam Toolbox` with `mapper_params_online_async.Yaml` file 
```
For Foxy - no slam
ros2 launch slam_toolbox online_async_launch.py params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true


For Humble - with Slam
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true
```

This will post `map` topic. Set `Rviz` configuration as follow:

![image](https://github.com/develtechmon/ROS2/assets/125783320/fdfcd2b9-c9f6-4625-a85d-efbdee854d00)

```
Fixed Frame : map
Robot Model :
     Description Topic : /robot_description

Map :
 Topic : /map
 Update Topic : /map_updates
```

Run following command to `move` our robot to start mapping
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

or

ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Move the robot around the area and once you're done please `return` the robot to its `original initial position in map` at which point it start to move.

Then save the `gazebo` map into your `/config/world/`

## Step 9: Save our Generated Map
Once you're done generating map, now it's time to save our `map`.

From `rviz` select `Add New Panel` and and select `SlamToolboxPlugin`

This will open `SlamToolboxPlugin`. From there enter following details

```
- Save Map - new_slam_map
- Serialize Map - new_slam_serial_map
```
* Click "serialize map"  button
* Click "save map" button 

or run below command to save the map
```
ros2 run nav2_map_server map_saver_cli -f map/maze ---> to save map
```

This will save the map into our `techdiffbot` directory

To clarify, the `*.yaml` and `*.pgm` together are the `old format`. The PGM contains the actual cell occupancy data while the YAML contains metadata such as the grid resolution and origin location. 

At working directory in this case is "techdiffbot" you should see multiple files has been created as follow:
```
1. new_slam_map.pgm
2. new_slam_map.yaml
3. new_slam_serial_map.data
4. new_slam_serial_map.posegraph
```

## Step 10: To start with Navigation Edit the `mapper_params_online_async.Yaml` file which point into our `saved map`

Disable `mode: mapping` and enable `mode: localization`
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: base_footprint
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
#mode: mapping <----------- disable this

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
mode: localization <----------- enable this

map_file_name: /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/new_slam_serial_map
map_start_at_dock: true
#map_start_pose: [0.0, 0.0, 0.0]

```
## Step 11: Save and build the packages
```
colcon build
. install/setup.bash
```

## Step 12: To start navigation run following command by sequence in every new terminal.
```
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/my_map 
rviz2 -d src/techdiffbot/rviz2/my_map.rviz

#For Foxy - no Slam
ros2 launch slam_toolbox online_async_launch.py params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true


#For Humble - with Slam
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

ros2 launch nav2_bringup navigation_launch.py use_sime_time:=true
```

from `rviz2` select `Map --> Topic --> /global_costmap/costmap` and `color Scheme --> costmap`

and select "2D pose goals" and select the map to start navigate the robot.


# Still Work in Progress...................
## Step 12: Start our `nav2 map server` 

Incase you havent open `rviz`, please open it first
```
rviz2 -d src/techdiffbot/rviz2/my_map.rviz
```
and run following command
```
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=new_slam_map.yaml -p use_sim_time:=true
```

And run below command to start the `lifecycle bringup map server` for above command to
Load image_file `./my_map_save.pgm`

```
ros2 run nav2_util lifecycle_bringup map_server
```
At this point, you should the saved "map" in our "rviz2"


## Step 13: Re-Launch `Gazebo world` with our Generated map
```
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/my_map 
```

From `rviz2` add following configuration
```
- Fixed Frame - map
- Map - Topic --> Durability Policy --> Transient Local
```

## Step 14: Run `nav2` using `amcl` method
```
ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true
ros2 run nav2_util lifecycle_bringup amcl
```

and select "2D pose estimate" to find best initial position in our "rviz2".
you may need to move the robot somwhere in the gazebo to find best location.

## Step 15 : To launch our Physical Robot
In RPI4 machine run following
```
ros2 launch techdiffbot launch_robot.launch.py 
ros2 launch techdiffbot lidar.launch.py
```

In Dev machine run following
```
rviz2 -d src/techdiffbot/rviz2/my_map.rviz

#For Humble - with Slam
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=false

ros2 launch nav2_bringup navigation_launch.py use_sime_time:=false
```
from `rviz2` select `Map --> Topic --> /global_costmap/costmap` and `color Scheme --> costmap`
and select "2D pose goals" and select the map to start navigate the robot.
