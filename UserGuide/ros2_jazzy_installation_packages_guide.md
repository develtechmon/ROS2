# User Guide

In this guide, i'm going to guide you on how to install `SLAM` and `Nav2` using ROS2 Jazzy
Please follow this setup carefully

## Step 1: Install Ros2 Jazzy 
```
locale  # check for UTF-8

locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade

sudo apt install ros-dev-tools

# For Development PC
sudo apt install ros-jazzy-desktop

# For RPI 
sudo apt install ros-jazzy-ros-base

# Possible values are: setup.bash, setup.sh, setup.zsh
source /opt/ros/jazzy/setup.bash
```

## Step 2: Install Colcon Packages
```
sudo apt install python3-colcon-common-extensions
```

## Step 3: Create our first Ros2 Package
```
mkdir -p talker_listener/src
cd src
ros2 pkg create --build-type ament_python talker_listener
colcon build
```

## Step 4: Install relevant ROS2 packages 
```
sudo apt-get install tree -y
sudo apt-get install ros-jazzy-xacro -y
sudo apt install ros-jazzy-joint-state-publisher-gui -y
sudo apt-get install ros-jazzy-teleop-twist-keyboard -y
sudo apt-get install ros-jazzy-teleop-twist-joy -y
sudo apt-get install ros-jazzy-gazebo-ros-pkgs -y 
sudo apt-get install ros-jazzy-robot-state -y
sudo apt-get install joystick jstest-gtk evtest -y
sudo apt install ros-jazzy-joy-tester -y
sudo apt-get install v4l-utils -y
sudo apt-get install ros-jazzy-twist-mux -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-transforms3d -y
sudo apt-get install ros-jazzy-key-teleop -y
sudo apt install ros-$ROS_DISTRO-plotjuggler-ros -y
sudo apt-get install ros-jazzy-rviz-imu-plugin -y
pip install pyserial 
sudo apt-get install ros-humble-rqt-robot-steering -y
sudo apt install gcc-12

This package for docker
sudo apt-get install cmake
sudo apt-get install curl
sudo apt-get install gazebo 
sudo apt-get install libglu1-mesa-dev
sudo apt-get install python3-pip
sudo apt-get install python3-pydantic
sudo apt-get install ros-jazzy-gazebo-ros
sudo apt-get install ros-jazzy-gazebo-ros-pkgs
sudo apt-get install ros-jazzy-joint-state-publisher
sudo apt-get install ros-jazzy-robot-localization
sudo apt-get install ros-jazzy-plotjuggler-ros
sudo apt-get install ros-jazzy-robot-state-publisher
sudo apt-get install ros-jazzy-ros2bag
sudo apt-get install ros-jazzy-rosbag2-storage-default-plugins
sudo apt-get install ros-jazzy-rqt-tf-tree
sudo apt-get install ros-jazzy-rmw-fastrtps-cpp 
sudo apt-get install ros-jazzy-rmw-cyclonedds-cpp 
sudo apt-get install ros-jazzy-slam-toolbox 
sudo apt-get install ros-jazzy-turtlebot3 
sudo apt-get install ros-jazzy-turtlebot3-msgs 
sudo apt-get install ros-jazzy-twist-mux 
sudo apt-get install ros-jazzy-usb-cam 
sudo apt-get install ros-jazzy-xacro
sudo apt-get install ros-jazzy-rmw-fastrtps-cpp
sudo apt-get install ros-jazzy-usb-cam
sudo apt-get install ros-jazzy-plotjuggler-ros
sudo apt-get install ruby-dev 
sudo apt-get install rviz 
sudo apt-get install tmux 
sudo apt-get install wget 
sudo apt-get install xorg-dev 
sudo apt-get install zsh
```

## Step 5: Install following packages for image rqt
```
sudo apt-get install v4l-utils ros-jazzy-v4l2-camera
sudo apt-get install ros-jazzy-image-transport-plugins ros-jazzy-rqt-image-view
sudo apt-get install ros-jazzy-rqt-image-view
```

## Step 6: Install following packages for cv2 bridge
```
sudo apt-get install ros-jazzy-cv-bridge
sudo apt install ros-jazzy-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

## Step 7: Install following packages for ros2_control
```
sudo apt-get install ros-jazzy-ros2-control -y
sudo apt-get install ros-jazzy-ros2-controllers -y
sudo apt-get install ros-jazzy-gazebo-ros2-control -y
sudo apt install ros-jazzy-controller-manager -y
```

## Step 8: Install following packages for slam 
```
sudo apt-get install ros-jazzy-slam-toolbox -y
```

## Step 9: To test our gazebo run following command
```
ros2 launch gazebo_ros gazebo.launch.py
```

## Step 10: Install following packages for nav2
```
sudo apt-get install ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-turtlebot3* -y
sudo apt-get install ros-jazzy-nav2* -y
sudo apt-get install ros-jazzy-tf2* -y
```

## Step 11: Clone for Serial and Diffdriver Controller
You may need to clone this library into your `techdiffbot` src directory by running following command
```
git clone https://github.com/joshnewans/diffdrive_arduino.git -b jazzy
git clone https://github.com/joshnewans/serial.git
cd ../
rosdep update && rosdep install --from-path src --ignore-src -y
```

## Step 12: Controller Manager
If you're using Foxy, plese use *.py Controller Manager in launch file
```
ros2 run controller_manager spawner.py diff_cont
ros2 run controller_manager spawner.py joint_broad
```

If you're using jazzy, please ignore *.py Controller Manager in launch file
```
ros2 run controller_manager spawner diff_cont
ros2 run controller_manager spawner joint_broad
```




