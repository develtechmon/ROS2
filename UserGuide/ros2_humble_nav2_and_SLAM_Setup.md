# Getting Started

Scenario, i really have an issues working with `C1 Slamtec` and `LD06` lidar. It's hard to get a fix localization of `map` during 
SLAM. The scan radius mapping is not fixed with respect to robot movement. 

The only way to get a fixed mapping is to force the Lidar Scanning operating to follow the odom and base_footprint.

Current `ros2 lidar` library tested so far, fail to get a fix positoin of lidar during mapping. In this userguide, i'm able to get 
a fix mapping. See below tutorial and guide.

Current this work with `LD06/19` Lidar Sensor

# Raspberry PI - Running Ubuntu 20 and ROS2 Humble

## Step 1: Download or Git clone this package

please follow these steps. Open your terminal
```
cd /home/jlukas/
mkdir -p ldrobot_lidar_ros2/src
cd src
git clone https://github.com/Myzhar/ldrobot-lidar-ros2.git
```
