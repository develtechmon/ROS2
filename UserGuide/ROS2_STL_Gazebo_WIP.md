Ros2 STL Gazebo

# Install This package first
```
sudo apt-get install python3-vcstool -- For vcs
sudo apt install ros-humble-geographic-msgs
```

# Install Mavros
```
sudo apt-get install ros-humble-mavros ros-humble-mavros-extras
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh

wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh --no-check-certificate --> To check without certificate

chmod a+x install_geographiclib_datasets.sh
./install_geographiclib_datasets.sh

sudo apt-get install ros-humble-rqt ros-humble-rqt-common-plugins ros-humble-rqt-robot-plugins
```

# Install Gazebo harmonic  - New Gazebo Type
```
sudo apt-get update
sudo apt-get install lsb-release wget gnupg
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```

# Install Microddsgen
```
sudo apt install default-jre
nocd Micro-XRCE-DDS-Gen
./gradlew assemble
```
# Add this to ~/.bashrc
```
export PATH=$PATH:/home/jlukas/Micro-XRCE-DDS-Gen/scripts
```

# Install ROs2 with Gazebo - harmonic 
```
cd ~/ros2_ws
wget https://raw.githubusercontent.com/ArduPilot/ardupilot_gz/main/ros2_gz.repos
vcs import --recursive src < ros2_gz.repos

export GZ_VERSION=garden

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r

cd ~/ros2_ws
colcon build --packages-up-to ardupilot_gz_bringup
```

# Iris Runway
```
ros2 launch ardupilot_gz_bringup iris_runway.launch.py
```

# Iris Maze
```
ros2 launch ardupilot_gz_bringup iris_maze.launch.py
```

Visit link:
```
https://ardupilot.org/dev/docs/ros2-gazebo.html
https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_DDS#installing-build-dependencies
https://gazebosim.org/docs/harmonic/install_ubuntu
https://micro-xrce-dds.docs.eprosima.com/en/stable/installation.html
https://ardupilot.org/dev/docs/ros-install.html#installing-mavros
```
