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

right_wheel_names: ['rightt_wheel_joint']
left_wheel_names: ['light_wheel_joint']
wheel_separation: 0.21
wheel_radius: 0.03405
```

## Step 3 : SLAM setup for mapping

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


## Step 4: Start Mapping

In your development `pc` or `laptop`, follow below step
```
1. In new terminal run Gazebo
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/my_block

2. In new terminal run Rviz
 rviz2

3. In new terminal run SLAM toolbox
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true (i'm using this mostly)

Above command is similar to below command. What make it different, is that one using launcher and other is run
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

4. From Rviz select
   Fixed Frame - map
   Map Topic - Map

   You will need hit the reset button if rviz didn't work properly and re-add the the function and select topic accordingly.
   RobotModel --> /robotdescription
   LaserScan --> /scan
   TF --> enable and shown only the base link, odom, base_footprint
   
5. In new terminal run Steam Joystick or Keyboard control to start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

`Move the robot` around the area and once you're done please `return the robot to its original initial
position` in rviz2 at which point it start to move, 

in this case you should stop at `map` and align it with `base_link` and `base_footprint` TF frame from rviz. This `TF` is referring to our
original position. For your information, `map TF` will be fixed at one postion, while `odom TF` will jumping around.

Next save the gazebo map into your `techdiffobt../config/world/` and name it as `my_block_world` and etc

## Step 5: Saved our SLAM Map

Once you're done generating map, now it's time to save our `map`.

From `rviz` select `Add New Panel` and and select `SlamToolboxPlugin`

This will open `SlamToolboxPlugin`. From there enter following details

```
- Save Map - my_block
- Serialize Map - my_block_serialize
```

Please ensure to tick the right `button` box under the `map` to ensure you can generate the map accordingly.

* Click "serialize map"  button
* Click "save map" button 

or run below command to save the map
```
ros2 run nav2_map_server map_saver_cli -f map/my_block ---> to save map
```

This will save the map into our `techdiffbot` directory

To clarify, the `*.yaml` and `*.pgm` together are the `old format`. The PGM contains the actual cell occupancy data while the YAML contains metadata such as the grid resolution and origin location. 

At working directory in this case is "techdiffbot" you should see multiple files has been created as follow:
```
1. my_block.pgm
2. my_block.yaml
3. my_block_serial.data
4. my_block_serial.posegraph
```

## Step 6 : SLAM setup for localization

To start with `localization` please enable `mode:localization` and disable `mode:mapping` inside `mapper_params_online_async.yaml` file as follow.
Here we're enabling `localization mode` to begin with.

open the `yaml` file
```
vi src/techdiffbot/config/mapper_params_online_async.yaml 
```

and Enable `localization` and Disable `mapping` mode as follow.
```
# ROS Parameters
odom_frame: odom
map_frame: map
#base_frame: ldlidar_base
base_frame: base_footprint 
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
#mode: mapping <---- Please disable this line to start localization

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
mode: localization <---- Please enable this line to start localization

map_file_name: /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/my_block_serial
map_start_at_dock: true
#map_start_pose: [0.0, 0.0, 0.0]
```
Then save and quit.

## Step 7: Start Navigation

In your development `pc` or `laptop`, follow below step
```
1. In new terminal run Gazebo
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/my_block

2. In new terminal run Rviz
 rviz2

3. In new terminal run SLAM toolbox
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true (i'm using this mostly)

Above command is similar to below command. What make it different, is that one using launcher and other is run
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

4. From Rviz select
   Fixed Frame - map
   Map Topic - Map

   You will need hit the reset button if rviz didn't work properly and re-add the the function and select topic accordingly.
   RobotModel --> /robotdescription
   LaserScan --> /scan
   TF --> enable and shown only the base link, odom, base_footprint

5. In new terminal run Nav2 (default command)
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true

Run below command to bringup the Navigation if you already have local copy of `navigation_launch.py` and `nav2_params.yaml` file and already edit the configuration.
Then run this command. However, in this package, i already edit the package for you. So no need to worry and you can safely run this command.
* ros2 launch techdiffbot navigation_launch.py use_sim_time:=true

6. From Rviz select
   Fixed Frame - map
   Map Topic - Global../Costmap
   Color Scheme - Costmap

9. Select 2D Goal Pose and start navigating
```

## Step 8: Start Navigation with AMCL

The advantage of using AMCL, is that we can set and estimate the position of our robot in the 3D Space and add the unknown object in real time. 
Let's try to run our robot using AMCL method as follow.

In your `development PC` pc, open new terminal and run following command first
Here we're launching our `SLAM_Toolbox` to activate the map detection in rviz. This run will show our previous saved map.
```
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true
```

From rviz, set the configuration similarly as mapping section as shown in `mapping` section.

Then start our `AMCL` command as follow.
```
ros2 launch nav2_bringup localization_launch.py map:=./my_block.yaml use_sim_time:=true
```
Once running this command. The terminal will prompt you to select `Intial pose` and from `rviz` select `2D pose estimate` button and 
adjust your robot position accordingly.

If your robot jumping around, kill the `slam_toolbox` run previously.

To start navigation with `AMCL`, open your new terminal and run following command and select the `2D Goal` to start navigating the robot.
```
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true
```
