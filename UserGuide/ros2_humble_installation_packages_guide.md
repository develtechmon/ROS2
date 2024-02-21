# User Guide

In this guide, i'm going to guide you on how to install `SLAM` and `Nav2` using ROS2 humble
Please follow this setup carefully

## Step 1: Install Ros2 Humble 
```
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

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update

sudo apt upgrade

sudo apt install ros-dev-tools

#sudo apt install ros-humble-desktop

sudo apt install ros-humble-ros-base

# Possible values are: setup.bash, setup.sh, setup.zsh
source /opt/ros/humble/setup.bash
```

## Step 2: Install Colcon Packages
```
sudo apt install python3-colcon-common-extensions
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
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
sudo apt-get install tree
sudo apt-get install ros-humble-xacro
sudo apt install ros-humble-joint-state-publisher-gui
sudo apt-get install ros-humble-teleop-twist-keyboard
sudo apt-get install ros-humble-teleop-twist-joy
sudo apt-get install ros-humble-gazebo-ros-pkgs 
sudo apt-get install ros-humble-robot-state
sudo apt-get install joystick jstest-gtk evtest
sudo apt install ros-humble-joy-tester
sudo apt-get install v4l-utils
sudo apt-get install ros-humble-twist-mux
```

## Step 5: Install following packages for image rqt
```
sudo apt-get install v4l-utils ros-humble-v4l2-camera
sudo apt-get install ros-humble-image-transport-plugins ros-humble-rqt-image-view
sudo apt-get install ros-humble-rqt-image-view
```

## Step 6: Install following packages for cv2 bridge
```
sudo apt-get install ros-humble-cv-bridge
sudo apt install ros-humble-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

## Step 7: Install following packages for ros2_control
```
sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros2-control
sudo apt install ros-humble-controller-manager
```

## Step 8: Install following packages for slam 
```
sudo apt-get install ros-humble-slam-toolbox
```

## Step 9: To test our gazebo run following command
```
ros2 launch gazebo_ros gazebo.launch.py
```

## Step 10: Install following packages for nav2
```
sudo apt-get install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*
sudo apt-get install ros-humble-nav2*
sudo apt-get install ros-humble-tf2*
```

## Step 11: Clone for Serial and Diffdriver Controller
You may need to clone this library into your `techdiffbot` src directory by running following command
```
git clone https://github.com/joshnewans/diffdrive_arduino.git -b humble
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

If you're using Humble, please ignore *.py Controller Manager in launch file
```
ros2 run controller_manager spawner diff_cont
ros2 run controller_manager spawner joint_broad
```



