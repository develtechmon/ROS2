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
sudo apt-get install ros-foxy-slam-toolbox
sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*
```
Remember there are two type of such as `Online` and `Asynchronous`.
For `Online` - we are working on a live data stream rather than recorded logs

For `Asynchronous` - Always process the most recent scan to avoid lagging, even if that means skipping scans

## Step 3: Copy the `Yaml` file for `Slam` configuration
```
cp -r /opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml My_Project/ROS2/rover/src/rover/config/
```

## Step 4: Edit the `Yaml` file with our Configuration
Here we're using `mapping` mode to start
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: base_footprint
scan_topic: /scan
use_map_saver: true
mode: mapping #localization
```

## Step 5: Build our `Package`
```
colcon build --symlink-install
source install/setup.bash
```

## Step 6: Launch `Gazebo world` with following command
```
ros2 launch rover gazebo.sim.launch.py world:=./src/rover/world/slam_obstacles
```

## Step 7: Launch `rviz2 world` with following command
```
rviz2 -d src/rover/config/slam_obstacles.rviz
```

## Step 8: Launch our `Slam Toolbox` with `YAML` file
```
ros2 launch slam_toolbox online_async_launch.py params_file:=./src/rover/config/mapper_params_online_async.yaml use_sim_time:=true
```

This will post `map` topic. From `Rviz2` select `Map` Topic `/map` and change the `Fixed Frame` to `map`

From views select `TopDownOrtho(rviz_default_plugins)`

run following command to start `mapping`
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## Step 9: Save our Generated Map
Once you're done generating map, now it's time to save our `map`.

From `rviz` select `Add New Panel` and got `slam_toolbox` and select `SlamToolboxPlugin`

This will open `SlamToolboxPlugin` and save the file into following field

- Save Map - my_map_save
- Serialize Map - my_map_serial

And the select `Save Map` and `Serialize Map` to save the map imto our `rover` directory

To clarify, the `*.yaml` and `*.pgm` together are the `old format`. The PGM contains the actual cell occupancy data while the YAML contains metadata such as the grid resolution and origin location.

## Step 10: Edit the `Yaml` file with our new Configuration with generated `Map`

```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: base_footprint
scan_topic: /scan
use_map_saver: true
mode: localization <----------

# if you'd like to immediately start continuing a map at a given pose
# or at the dock, but they are mutually exclusive, if pose is given
# will use pose
map_file_name: /home/jlukas/My_Project/ROS2/rover/my_map_serial <---------
# map_start_pose: [0.0, 0.0, 0.0]
map_start_at_dock: true <---------
```
## Step 11: Launch our `Slam Toolbox` with update `YAML` file
```
ros2 launch slam_toolbox online_async_launch.py params_file:=./src/rover/config/mapper_params_online_async.yaml use_sim_time:=true
```

## Step 12: Start our `nav2 map server` to our `my_map_save.yaml` file
```
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=my_map_save.yaml -p use_sim_time:=true
```

And run below command to start the `lifecycle bringup map server` for above command to
Load image_file `./my_map_save.pgm`

```
ros2 run nav2_util lifecycle_bringup map_server
```

## Step 13: Re-Launch `Gazebo world` with our Generate map
```
ros2 launch rover gazebo.sim.launch.py world:=./src/rover/world/slam_obstacles
```

From `rviz2` add following configuration
- Fixed Frame - map
- Map - Topic --> Durability Policy --> Transient Local

## Step 14: Run `nav2` using `amcl` method
```
ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true

and then run

ros2 run nav2_util lifecycle_bringup amcl
```

