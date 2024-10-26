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

Let's modify `ldlidar.launch.py`. Here i just disable `rsp_node` function.
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

Next, let's modify 



