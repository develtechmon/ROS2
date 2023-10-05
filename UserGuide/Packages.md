## Getting Started

We're going to install `robot_state_publisher` package. Please run this command
```
sudo apt install ros-humble-xacro
sudo apt install ros-humble-joint-state-publisher-gui
sudo apt-get install ros-humble-teleop-twist-keyboard
sudo apt-get install ros-humble-teleop-twist-joy
sudo apt-get install ros-humble-gazebo-ros-pkgs
sudo apt-get install ros-humble -robot-state
```

This is to install libraries needed for our Rpi
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip

sudo pip install RPi.GPIO  
```

To install `lidar sensor` for RPI
```
pip3 install adafruit-circuitpython-vl53l0x
```
This library is used for `cv2` images and video. Because sometime image stream using `cv2` will freeze. To resolve this, please use this library

Link as follow:
```
https://github.com/ros2/rclcpp/issues/1335
```

Library as follow:
```
sudo apt install ros-humble-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```