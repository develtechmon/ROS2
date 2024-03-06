Ubuntu 18.04.4 LTS
Release 18.04
Codename Bionic

# SITL Installation

1. Install Python 2.7 Pip package
```
sudo apt-get update
sudo apt-get upgrade

curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py -k
sudo python get-pip.py
pip --version
```

Once completed run velow command to to determine if installed pip is refer to python 2.7 using below command
```
whereis pip
```

2. Install python 3 pip
```
sudo apt-get update
sudo apt install python3-pip
```
Once completed run python to check if pip installed pip is refer to python 3.6 using below command
```
whereis pip
```

3. Install Ardupilot and relevant packages
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git
sudo pip install pexpect
sudo pip install future
sudo pip install pyserial
sudo pip install dronekit
sudo pip install MAVProxy
sudo pip install keyboard

git config --global http.sslverify false
git clone https://github.com/ArduPilot/ardupilot

cd ardupilot
git submodule update --init --recursive

./Tools/environment_install/install_prereqs_ubuntu.sh -y
```

4. Load the `profile`
```
. ~/.profile (Space in between . and ~ - reload this profile if sim_vehicle not found)
```



# Gazebo 9
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

If you can't add the key, you can run below command to run it manually
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654

If you can add the key, you can run below command to ping the server
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

Next we're going to fly our `drone` in Gazebo. Run following command in new terminal
```
gazebo iris_arducopter_runaway.world

cd ardupilot/ArduCopter
../Tools/autotest/sim_vehicle.py -f gazebo-iris --console --map
```

If you encounter error `VMware: vmw_ioctl_command error Invalid argument`. Run following command to remove
this error

1. Downgrade `GL_VERSION` from 3.3 to 2.1. This method will work better and Gazebo performance also good
```
echo "export SVGA_VGPU10=0" >> ~/.bashrc
```

2. Disable Graphic Acceleration in VMWARE. This method OK but will reduce 3D performance in Gazebo
```
Untick Accelerate 3D Graphics.
```
Check below link for good reference
```
https://robocademy.com/2020/05/02/solved-opengl-issues-with-gazebo-and-vmware/
```
