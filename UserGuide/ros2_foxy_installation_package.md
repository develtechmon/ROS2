## Install python3 package
sudo apt-get install python3-pip

## Install ros2-foxy
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
sudo apt install ros-foxy-desktop python3-argcomplete
sudo apt install ros-dev-tools

-- Replace ".bash" with your shell if you're not using bash
-- Possible values are: setup.bash, setup.sh, setup.zsh
source /opt/ros/foxy/setup.bash

## Install Colcon Package
sudo apt install python3-colcon-common-extensions
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

## Make our first package
sudo apt-get install tree
mkdir -p talker_listener/src
cd src
ros2 pkg create --build-type ament_python talker_listener
colcon build

## Install following packages
sudo apt-get install ros-foxy-xacro
sudo apt install ros-foxy-joint-state-publisher-gui
sudo apt-get install ros-foxy-teleop-twist-keyboard
sudo apt-get install ros-foxy-teleop-twist-joy
sudo apt-get install ros-foxy-gazebo-ros-pkgs 
sudo apt-get install ros-foxy-robot-state
sudo apt-get install joystick jstest-gtk evtest
sudo apt install ros-foxy-joy-tester
sudo apt-get install v4l-utils

## Install following packages for image rqt
sudo apt-get install v4l-utils ros-foxy-v4l2-camera
sudo apt-get install ros-foxy-image-transport-plugins ros-foxy-rqt-image-view
sudo apt-get install ros-foxy-rqt-image-view

## Install following packages for cv2 bridge
sudo apt-get install ros-foxy-cv-bridge
sudo apt install ros-foxy-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

## Install following packages for ros2_control
sudo apt-get install ros-foxy-ros2-control
sudo apt-get install ros-foxy-ros2-controllers
sudo apt-get install ros-foxy-gazebo-ros2-control
sudo apt install ros-foxy-controller-manager

## Install following packages for slam 
sudo apt-get install ros-foxy-slam-toolbox

## To test our gazebo run following command
ros2 launch gazebo_ros gazebo.launch.py

## Install following packages for nav2
sudo apt-get install ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-turtlebot3*
sudo apt-get install ros-foxy-nav2*
sudo apt-get install ros-foxy-tf2*

## Clone 
git clone https://github.com/joshnewans/diffdrive_arduino.git 
git clone https://github.com/joshnewans/serial.git
cd ../
rosdep update && rosdep install --from-path src --ignore-src -y

## Controller Manager for Foxy
ros2 run controller_manager spawner.py diff_cont
ros2 run controller_manager spawner.py joint_broad

## To start mapping run following command. Please ensure mode mapping is enabled
ros2 launch slam_toolbox online_async_launch.py params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped

## To start mapping run following command. Please ensure mode mapping is disabled and mode localization is enabled
colcon build
ros2 launch techdiffbot gazebo.sim.launch.py world:=./src/techdiffbot/world/my_map 
rviz2
ros2 launch slam_toolbox online_async_launch.py params_file:=src/techdiffbot/config/mapper_params_online_async.yaml use_sim_time:=true
ros2 launch nav2_bringup navigation_launch.py use_sime_time:=true
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map odom << run this to solve missing odom and base link issues after launching bringup nav2
