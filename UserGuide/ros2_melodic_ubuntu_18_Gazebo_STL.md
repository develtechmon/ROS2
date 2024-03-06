Ubuntu 18.04.4 LTS
Release 18.04
Codename Bionic

Gazebo 9
```
1. sudo apt install python-opencv=3.2.0+dfsg-4ubuntu0.1
```

```
2. sudo apt install gazebo9 libgazebo9-dev
sudo vi .ignition/fuel/config.yaml
Replace name url: https://fuel.ignitionrobotics.org
save and quit
```

```
3. git clone https://github.com/dronedojo/ardupilot_gazebo
cd ardupilot_gazebo
mkdir build
cd build
sudo apt install cmake
cmake ..
make -j4
sudo make install
```
```
sudo vi ~jlukas/.bashrc and add following line
export GAZEBO_RESOURCE_PATH="/home/dronedojo/courseRoot/ardupilot_gazebo":"/home/dronedojo/courseRoot/ardupilot_gazebo/worlds":"/usr/share/gazebo-9"
export GAZEBO_MODEL_PATH="/home/dronedojo/courseRoot/ardupilot_gazebo/models":"/usr/share/gazebo-9/models"

source /usr/share/gazebo-9/setup.sh
```

Then we need to edit aboive setup.sh file
```
sudo vi  /usr/share/gazebo-9/setup.sh
Please remove 
export GAZEBO_RESOURCE_PATH
export GAZEBO_MODEL_PATH

save and quit
```

Next we're going to install ros2 melodic
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update
sudo apt install ros-melodic-desktop-full

Add this to .bashrc:
source /opt/ros/melodic/setup.bash
sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
sudo apt install python-rosdep
sudo rosdep init
rosdep update

sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
```

