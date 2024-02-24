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

## For real robot
```
base_frame: ldlidar_base <---- This is our ldlidar_base that match to our Lidar URDF Link that hold the Lidar
```

## For Simulation
```
base_frame: base_footprint <---- For simulation, we're using base_footprint
```

## Step 2 : Change Wheel Position
I find this is quite strange because `right wheels` and `left wheel motor` didn't match similarly as simulation. 
To solve this, i swap left and right `wheel` the parameters in `src/techdiffbot/config/my_controllers.yaml`

## For real robot
```
base_frame_id: base_link

right_wheel_names: ['left_wheel_joint']
left_wheel_names: ['right_wheel_joint']
wheel_separation: 0.21
wheel_radius: 0.03405
```

## For simulation
```
base_frame_id: base_link

right_wheel_names: ['reft_wheel_joint']
left_wheel_names: ['light_wheel_joint']
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

## Step 4 : Copy Nav2 params, because we're going to launch it locally inside our `techdiffbot`
Copy this file to our working space directory
```
cp -r /opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml ../config/
cp -r /opt/ros/humble/share/nav2_bringup/launch/navigation_launch.py ../launch/
```

And modify this file accordingly as follow

## For Simulation
`nav2_params.yaml`
```
Keep this parameter as it's
base_frame_id: "base_footprint"
robot_base_frame: base_link
```

`navigation_launch.py`
```
bringup_dir = get_package_share_directory('techdiffbot') # changes i made here to add directory name
default_value=os.path.join(bringup_dir, 'config', 'nav2_params.yaml') ,  ## changes i made here - add config
```
## For Real Robot
`nav2_params.yaml`
```
Keep this parameter below
base_frame_id: "ldlidar_base"
robot_base_frame: ldlidar_link
```

`navigation_launch.py`
```
bringup_dir = get_package_share_directory('techdiffbot') # changes i made here to add directory name
default_value=os.path.join(bringup_dir, 'config', 'nav2_params.yaml') ,  ## changes i made here - add config
```

## Step 4 : Set fixed `bus ID` to our Arduino port.
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

## For Simulation
To start with `mapping` please enable `mode:mapping` inside `mapper_params_online_async.yaml` file as follow Here we're using mapping mode to start
```
# ROS Parameters
odom_frame: odom
map_frame: map
#base_frame: ldlidar_base
base_frame: base_footprint <--------- For simulation, we're enabling this
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
mode: mapping 

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
#mode: localization


```
## For Real Robot
To start with `mapping` please enable `mode:mapping` inside `mapper_params_online_async.yaml` file as follow Here we're using mapping mode to start
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: ldlidar_base <---- This is our ldlidar_base that match to our Lidar URDF Link that hold the Lidar
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
mode: mapping 

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
#mode: localization
```

From top directory run following command to compile all the changes that we've made just now. 
```
colcon build
. install/setup.bash
```

## Step 6 : To start  mapping our environment.

Follow below command by sequence.

## For simulation
```
1. In new terminal run Gazebo
ros2 launch techdiffbot gazebo.sim.launch.py  world:=./src/techdiffbot/world/my_maze 

2. In new terminal run Rviz
rviz2 -d src/techdiffbot/rviz2/my_maze.rviz 

3. In new terminal run SLAM toolbox
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

Above command is similar to below command. What make it different, is that one using launcher and other is run
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

4. From Rviz select
   Fixed Frame - map
   Map Topic - Map

5. In new terminal run Joystick or Keyboard control start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```


## For Real Robot
```
1. In new terminal run Gazebo
ros2 launch techdiffbot launch_robot.launch.py

2. In new terminal run Rviz
rviz2 

3. In new terminal run Lidar.  Here we're using `ldlidar_link` as our lidar_frame to ensure it matches with our URDF file
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=ldlidar_link

4. In new terminal run SLAM toolbox
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

Above command is similar to below command. What make it different, is that one using launcher and other is run
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=false

5. From Rviz select
   Fixed Frame - map
   Map Topic - Map

6. In new terminal run Joystick or Keyboard control start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

7. Might consider to run this commad to have a static transform - optional !
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 odom ldlidar_base
```

Move the robot around the area and once you're done please return the robot to its `original initial position in map` at which point it start to move.
Then save the `gazebo` map into your `/config/world/`

## Step 7 : Saved our SLAM Map
Once you're done generating map, now it's time to save our `map`.

From `rviz` select `Add New Panel` and and select `SlamToolboxPlugin`

This will open `SlamToolboxPlugin`. From there enter following details

```
- Save Map - maze_map
- Serialize Map - maze_map_serial
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
1. maze_mapp.pgm
2. maze_mapp.yaml
3. maze_map_serial.data
4. maze_map_serial.posegraph
```


## Step 8 : To start navigation, enable followig mode 

## For Simulation
To start with `navigation` please enable `mode:localization` and disable `mode: mapping` inside `mapper_params_online_async.yaml` file.
```
# ROS Parameters
odom_frame: odom
map_frame: map
#base_frame: ldlidar_base
base_frame: base_footprint <--------- For simulation, we're enabling this
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
#mode: mapping 

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
mode: localization

map_file_name: /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/my_maze_serial
map_start_at_dock: true
#map_start_pose: [0.0, 0.0, 0.0]

```
## For Real Robot
To start with `mapping` please enable `mode:mapping` inside `mapper_params_online_async.yaml` file as follow Here we're using mapping mode to start
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: ldlidar_base <---- This is our ldlidar_base that match to our Lidar URDF Link that hold the Lidar
scan_topic: /scan
use_map_saver: true

# 1: To start with mapping - enable mapping mode below
#mode: mapping 

# 2: After completing mapping, disable "mode: mapping" and enable "mode: localization" and use below command
mode: localization

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

## For simulation
```
1. In new terminal run Gazebo
ros2 launch techdiffbot gazebo.sim.launch.py  world:=./src/techdiffbot/world/my_maze 

2. In new terminal run Rviz
rviz2 -d src/techdiffbot/rviz2/my_maze.rviz 

3. In new terminal run SLAM toolbox
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

Above command is similar to below command. What make it different, is that one using launcher and other is run
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true

4. From Rviz select
   Fixed Frame - map
   Map Topic - Map

5. In new terminal run Joystick or Keyboard control start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

6. In new terminal run Nav2
ros2 launch  techdiffbot navigation_launch.py use_sim_time:=true

Run below command to bringup the Navigation if you already have local copy of `navigatio_launch.py` and `nav2_params.yaml` file and already edit the configuration. Then run this command
* ros2 launch techdiffbot navigation_launch.py use_sim_time:=true

7. From Rviz select
   Fixed Frame - map
   Map Topic - Global../Costmap
   Color Scheme - Costmap

8. Select 2D Goal Pose and start navigating
```


## For Real Robot
```
1. In new terminal run Gazebo
ros2 launch techdiffbot launch_robot.launch.py

2. In new terminal run Rviz
rviz2 

3. In new terminal run Lidar.  Here we're using `ldlidar_link` as our lidar_frame to ensure it matches with our URDF file
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=ldlidar_link

4. In new terminal run SLAM toolbox
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/techdiffbot/config/mapper_params_online_async.yaml

Above command is similar to below command. What make it different, is that one using launcher and other is run
* ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=false

5. From Rviz select
   Fixed Frame - map
   Map Topic - Map

6. In new terminal run Joystick or Keyboard control start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

7. In new terminal run Nav2
ros2 launch  techdiffbot navigation_launch.py use_sim_time:=false

Run below command to bringup the Navigation if you already have local copy of `navigation_launch.py` and `nav2_params.yaml` file and already edit the configuration. Then run this command
ros2 launch techdiffbot navigation_launch.py use_sim_time:=false

8. From Rviz select
   Fixed Frame - map
   Map Topic - Global../Costmap
   Color Scheme - Costmap

9. Select 2D Goal Pose and start navigating

```

And then pres 2D Goal pose to start navigation
```

