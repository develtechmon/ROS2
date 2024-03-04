# Getting Started

This userguide demonstrate on how to setup ros2_control with our actual robot in `RPI` our Robot

## 1. Clone following packages
```
cd techdiffbot/src
git clone https://github.com/joshnewans/diffdrive_arduino.git -b humble
git clone https://github.com/joshnewans/serial.git
ls
```
and install following libraries
```
sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros2-control
```
Under your directory you should see following directory in your working space
```
diffdrive_arduino serial techdiffbot 
```
and then run below command to install and solve the dependecies issues:
```
cd ../
rosdep update && rosdep install --from-path src --ignore-src -y
colcon build --symlink-install
```

## 2. Download and setup our Arduino Serial.

Run below command to enable `serial access` in our `RPI` or `VM Ubuntu` machine.
```
sudo adduser $USER dialout

or

sudo usermod -a -G dialout jlukas
```
and reboot to enable the serial access.

Then download below library packages into your `Main PC`.
```
git clone https://github.com/joshnewans/ros_arduino_bridge.git
```

Then open your `Arduino` and open the download packages above. In this case search for `ROSArduinoBridge`.
Please check below link to modify the Arduino pin accordingly

```
https://github.com/develtechmon/ROS2/blob/main/UserGuide/ros2_control_arduino_setup.md
```

and select the arduino port and board and then upload the program.

Plug out your `Arduino` from your main pc and connect it into `RPi` usb port.

## 3. Open your RPI
At this stage, your `Arduino` with dc motor connected should already connected to `RPI`. To test our motor install `pyserial-miniterm`
as follow if you don't have this install before this.
```
sudo apt-get install python3-serial
```

To run with local echo enabled run following command
```
pyserial-miniterm -e <serial port> <baud rate>

pyserial-miniterm -e /dev/ttyUSB0 57600
```






