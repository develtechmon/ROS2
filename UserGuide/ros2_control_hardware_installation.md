# Getting Started

This userguide demonstrate on how to setup ros2_control with our actual robot.

## 1. Clone following packages
```
cd robot_ws/src
git clone https://github.com/joshnewans/diffdrive_arduino
git clone https://github.com/joshnewans/serial

ls
```
and you should see following directory in your working space
```
diffdrive_arduino serial articubot serial_motor_demo
```
and then run
```
git pull
cd ../../
colcon build --symlink-install
```
## 2. Install following libraries
```
sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros2-control
```
