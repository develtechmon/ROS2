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
base_frame: base_footprint
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

## Step 3 : Change `src/techdiffbot/urdf/core.robot.xacro` file parameter
To ensure we're using `correct` lidar link, we have to modify `link` and `joint name` parameter under `Lidar` section
to ensure it's recognizable and work with our `ldlidar_base` and `ldlidar_link` above.

Please check `Lidar` section at `core.robot.xacro` on how to setup this parameter.
```

  <!-- LIDAR CASE JOINT -->
    <joint name="lidar_joint" type="fixed">
        <parent link="chassis_link"/>
        <child link="ldlidar_base"/>
        <origin xyz="0.0 0.0 0.1" rpy="0.0 0.0 0.0"/>
    </joint>

    <!-- LIDAR CASE LINK -->
    <link name="ldlidar_base"> <-------------- Our ldlidar_base
    <visual>
        <geometry>
            <box size="0.08 0.18 0.095"/>
        </geometry>
        <material name="red"/>
    </visual>

    <collision>
        <geometry>
            <box size="0.08 0.18 0.095"/>
        </geometry>
    </collision>
    <xacro:inertial_box mass="0.03" x="0.08" y="0.18" z="0.095">
        <origin xyz="0.0 0.0 0.0" rpy="0.0 0.0 0.0"/>
    </xacro:inertial_box>
    </link>

  <gazebo reference="ldlidar_base"> <-
      <material>Gazebo/Red</material>
  </gazebo>

  <!-- LIDAR  JOINT -->
  <joint name="lidar_case_joint" type="fixed">
      <origin xyz="0.0 0.0 0.055 " rpy="0.0 0.0 4.71239"/>
      <parent link="ldlidar_base"/>
      <child link="ldlidar_link"/>
  </joint>

  <!-- LIDAR LINK -->
  <link name="ldlidar_link"> <-------------- Our lidar_fram= ldlidar_link
  <visual>
      <!-- <origin xyz="0.0 0.0 0.0" rpy="0.0 0.0 0.0"/> -->
      <geometry>
          <cylinder radius="0.0175" length="0.0175"/>
      </geometry>
      <material name="blue"/>
  </visual>

  <collision>
      <geometry>
          <cylinder radius="0.0175" length="0.0175"/>
      </geometry>
  </collision>
  <xacro:inertial_cylinder mass="0.1" length="0.0175" radius="0.0175">
      <origin xyz="0.0 0.0 0.0" rpy="0.0 0.0 0.0"/>
  </xacro:inertial_cylinder>
  </link>

  <gazebo reference="ldlidar_link">
      <material>Gazebo/Blue</material>
  </gazebo>
```

## Step 4 : Copy Nav2 params, because we're going to launch it locally inside our `techdiffbot`
Copy this file to our working space directory
```
cp -r /opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml ../config/
cp -r /opt/ros/humble/share/nav2_bringup/launch/navigation_launch.py ../launch/
```

And modify this file accordingly as follow

##  For Real Robot
`nav2_params.yaml`
```
base_frame_id: "base_footprint"
robot_base_frame: base_link
```

`navigation_launch.py`
```
bringup_dir = get_package_share_directory('techdiffbot') # changes i made here to add directory name
default_value=os.path.join(bringup_dir, 'config', 'nav2_params.yaml') ,  ## changes i made here - add config
```

## Step 5 : Set fixed `bus ID` to our Arduino port.
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

## Step 6 : Clone `Lidar Packages` that comprises of `SLAM` and `NAv2` packages

This is another example i use that quite helpful on how to perform `SLAM` and `NAv2`.
Check this link : https://github.com/Myzhar/ldrobot-lidar-ros2/tree/main

Clone the repository in your ROS2 workspace:
```
mkdir -p ldrobot_lidar_ros2/src
cd src
git clone https://github.com/Myzhar/ldrobot-lidar-ros2.git
```

Add dependencies
```
sudo apt install libudev-dev
```

Install the udev rules
```
cd ~/ros2_ws/src/ldrobot-lidar-ros2/scripts/
./create_udev_rules.sh
```
Build the packages
```
cd ~/ldrobot_lidar_ros2/
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
```

Update the environment variables:
```
echo source $(pwd)/install/local_setup.bash >> ~/.bashrc
source ~/.bashrc
```

## Step 7 : Modify the parameters inside the `ldrobot-lidar-ros2` packages

`ldlidar_node/launch/ldlidar.launch.py`
```
# Launch Nav2 Lifecycle Manager
#ld.add_action(rsp_node) <--- disable this line
```

`ldlidar_node/launch/ldlidar_slam.launch.py`
```
# Start RVIZ2
#ld.add_action(rviz2_node) <--- disable this line
```

`ldlidar_node/params/slam_toolbox.yaml`
To start with `mapping` please enable `mode:mapping` inside `slam_toolbox.yaml` file as follow Here we're using mapping mode to start
```
#base_frame: ldlidar_base
base_frame: base_footprint <----- Change to base_footprint
scan_topic: /scan
use_map_saver: true
mode: mapping #localization <---- Enable mapping to start mapping
```

From top directory `ldrobot-lidar-ros2` run following command to compile all the changes that we've made just now. 
```
colcon build
. install/setup.bash
```

## Step 8 : Copy file into `techdiffbot` directory 

At this step, copy following file
```
cp -r /opt/ros/humble/share/nav2_bringup/params/nav2_params.yaml ../config/
cp -r /opt/ros/humble/share/nav2_bringup/launch/navigation_launch.py ../launch/

cp -r /home/jlukas/Desktop/My_Project/ldrobot_lidar_ros2/src/ldrobot-lidar-ros2/ldlidar_node/launch/ldlidar_slam.launch.py ../launch/
cp -r /home/jlukas/Desktop/My_Project/ldrobot_lidar_ros2/src/ldrobot-lidar-ros2/ldlidar_node/params/lifecycle_mgr_slam.yaml ../config
```

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

`ldlidar_slam.launch.py`
```
package_name="techdiffbot" <------- Add our package name
lc_mgr_config_path = os.path.join(get_package_share_directory(package_name),'config','lifecycle_mgr_slam.yaml') <---- Add this line to point to our `lifecycle_mgr_slam` file that we copy earlier.

arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_footprint'] <---- Change our Fake Odom Publisher to `odom` and `ldlidar_base`

# Start RVIZ2
#ld.add_action(rviz2_node) <---------- Disable this line
```

From top directory `techdiffbot` run following command to compile all the changes that we've made just now. 
```
colcon build
. install/setup.bash
```


## Step 9 : To start  mapping our environment.

Follow below command by sequence.

```
1. ros2 launch techdiffbot launch_robot.launch.py
2. ros2 launch techdiffbot ldlidar_slam.launch.py 

3. From Rviz select
   Fixed Frame - map
   Map Topic - Map

4. In new terminal run Joystick or Keyboard control start Mapping
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped
```

Move the robot around the area and once you're done please return the robot to its `original initial position in map` at which point it start to move.
Then save the `gazebo` map into your `/config/world/`

## Step 10 : Saved our SLAM Map
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


## Step 11 : To start navigation, enable followig mode 

To start with `navigation` please enable `mode:localization` and disable `mode: mapping` inside `slam_toolbox.yaml` file as follow Here we're using mapping mode to start

`ldlidar_node/params/slam_toolbox.yaml`
```
#base_frame: ldlidar_base
base_frame: base_footprint <----- Change to base_footprint
scan_topic: /scan
use_map_saver: true
mode: localization #mapping <---- Enable localization to start navigation

# if you'd like to immediately start continuing a map at a given pose
# or at the dock, but they are mutually exclusive, if pose is given
# will use pose
map_file_name: /home/jlukas/Desktop/My_Project/ROS2/techdiffbot/my_maze_serial
map_start_at_dock: true
# map_start_pose: [0.0, 0.0, 0.0]
```

From top directory `ldrobot-lidar-ros2` run following command to compile all the changes that we've made just now. 
```
colcon build
. install/setup.bash
```

## Step 12 : To start with navigation of our environment

Follow below command by sequence.
```
1. ros2 launch techdiffbot launch_robot.launch.py
2. ros2 launch techdiffbot ldlidar_slam.launch.py 

3. From Rviz select
   Fixed Frame - map
   Map Topic - Global../Costmap
   Color Scheme - Costmap

4. In new terminal run Joystick or Keyboard control start Navigation or control emergency
ros2 launch techdiffbot joystick.control.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

5. In new terminal run Nav2
ros2 launch  techdiffbot navigation_launch.py use_sim_time:=false

Run below command to bringup the Navigation if you already have local copy of `navigation_launch.py` and `nav2_params.yaml` file and already edit the configuration. Then run this command
ros2 launch techdiffbot navigation_launch.py use_sim_time:=false

6. Select 2D Goal Pose and start navigating
```

And then pres 2D Goal pose to start navigation
```

