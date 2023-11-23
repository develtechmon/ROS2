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

## 3. Download and setup our Arduino library

Run below command to enable `serial access`
```
sudo adduser $USER dialout
```
and reboot to enable the serial access.

Then download below library packages into your `Main PC`.
```
git clone https://github.com/joshnewans/ros_arduino_bridge.git
```

Then open your `Arduino` and open the download packages above. In this case search for `ROSArduinoBridge` 
and select the arduino port and board and then upload the program.

Plug out your `Arduino` from your main pc and connect it into `RPi` usb port.

## 3. Open your RPI
At this stage, your `Arduino` with dc motor connected should already connected to `RPI`. To test our motor install `minterm`
as follow if you don't have this install before this.
```
sudo apt-get install python3-serial
```

To run with local echo enabled run following command
```
miniterm -e <serial port> <baud rate>

miniterm -e /dev/ttyUSB0 57600
```






