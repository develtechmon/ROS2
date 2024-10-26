# Getting Started

Scenario, i really have an issues working with `C1 Slamtec` and `LD06` lidar. It's hard to get a fix localization of `map` during 
SLAM. The scan radius mapping is not fixed with respect to robot movement. 

The only way to get a fixed mapping is to force the Lidar Scanning operating to follow the odom and base_footprint.

Current `ros2 lidar` library tested so far, fail to get a fix positoin of lidar during mapping. In this userguide, i'm able to get 
a fix mapping. See below tutorial and guide.

Current this work with `LD06/19` Lidar Sensor

# Raspberry PI - Running Ubuntu 20 and ROS2 Humble

This package is based on this tutorial. highhly suggest to open this document 
and use it as reference for installation process.

```
https://github.com/Myzhar/ldrobot-lidar-ros2/tree/main
```

## Step 1: Download or Git clone this package

please follow these steps. Open your terminal:

```
cd /home/jlukas/
mkdir -p ldrobot_lidar_ros2/src
cd src
git clone https://github.com/Myzhar/ldrobot-lidar-ros2.git
```


## Step 2: Install the depdencies

Do the following to install this package

```
sudo apt install libudev-dev
cd ~/ros2_ws/src/ldrobot-lidar-ros2/scripts/
./create_udev_rules.sh
```

Install depedenceis
```
cd ~/ldrobot_lidar_ros2/
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
```

Update the environment
```
echo source $(pwd)/install/local_setup.bash >> ~/.bashrc
source ~/.bashrc
```

## Step 3 : Modify the files

To ensure it works with `bumperbot_ws` that i buuild, we need to adapt this parameters to match with our robot and also to solve non `fix` localization of lidar during mapping.
Please do the following

Go to `ldlidar-lidar-ros2` directory that we created earlier
```
cd /ldrobot_lidar_ros2/src/ldrobot-lidar-ros2/ldlidar_node
```

### 3.1 Let's modify `ldlidar.launch.py`. Here i just disable `rsp_node` function.
```
# Define LaunchDescription variable
ld = LaunchDescription()

# Launch arguments
ld.add_action(declare_node_name_cmd)

# Launch Nav2 Lifecycle Manager
#ld.add_action(rsp_node) <---------------Disable this line

# LDLidar Lifecycle node
ld.add_action(ldlidar_node)

```

### 3.2 Next, let's modify `params/slam_toolbox.yaml` and create a copy for our robot name `params/slam_toolbox_tech.yaml`

Then open 
```
vi slam_toolbox_tech.yaml
```

and modify the content as follow
```
# ROS Parameters
odom_frame: odom
map_frame: map
base_frame: ldlidar_base --> change to base_footprint
scan_topic: /scan
use_map_saver: true
mode: mapping #localization
```

## 3.2 Then modify `ldlidar_slam.launch.py` and create a copy for our robot named `ldlidar_slam_tech.launch.py`

Then open
```
vi ldlidar_slam_tech.launch.py
```

Then modify the content inside this file as follow
```
# Fake odom publisher
fake_odom = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_transform_publisher',
    output='screen',
    arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_footprint'] <------ Change to base_footprint to match with our robot urdf
)

# Define LaunchDescription variable
ld = LaunchDescription()

# Launch Nav2 Lifecycle Manager
ld.add_action(lc_mgr_node)

# Launch SLAM Toolbox node
ld.add_action(slam_toolbox_node)

# Launch fake odom publisher node
ld.add_action(fake_odom)

# Call LDLidar launch
ld.add_action(ldlidar_launch)

# Start RVIZ2
#ld.add_action(rviz2_node) <----------------- Disable rviz2

return ld
```

## Step 4 : Build pakages

Run below command to build our packages
```
cd ~ldrobot_lidar_ros2
colcon build
```


## Step 5 : Command I use for this section

To manually run using command line to start our slam toolbox and remap the `scan to ldlidar_nde`.
Tested on PC so far

````
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/bumperbot_bringup/config/mapper_params_online_async.yaml -r /scan:=/ldlidar_node/scan
````
