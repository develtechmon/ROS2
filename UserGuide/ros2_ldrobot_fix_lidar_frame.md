# Getting Started

This is userguide on how i establish a fix frame in `ld06` lidar which later used for SLAM and localization.
This package is based on `ldrobot-lidar-ros2`.

This is an extension userguide from this guide
```
https://github.com/develtechmon/ROS2/blob/main/UserGuide/ros2_humble_nav2_and_SLAM_Setup.md
```

What i did here, i separate the `ldlidar_with_mgr_tech.launch.py` with `slam` command. You can follow,
this userguide on how i set this separation and how i launch the `lldiar_with_mgr_tech.launh.py` using command
line and `slam  script`.

## Step 1 : Git Clone 

I've created modified version of `ldrobot ld06`. You can clone it into your directory annd follow this setup

Install this depedencies packages
```
sudo apt install libudev-dev
```

Then clone this package
```
cd ~
git clone https://github.com/develtechmon/ldrobot_lidar_ros2.git
cd ldrobot_lidar_ros2

rosdep install --from-paths src --ignore-src -r -y
colcon build
```

upon successfull build, you can consider to add this package into `bashrc script`
```
echo source $(pwd)/install/local_setup.bash >> ~/.bashrc
source ~jlukas/.bashrc
```

## Step 2 : Run and Test our SLAM in PC

### Step 2.1 - Option 1 : Run SLAM Directly

To run `SLAM` directly
```
ros2 launch ldlidar_node ldlidar_slam.launch.py
```

This will launch `rviz2` directly. You can select `map` from rviz and move the `lidar`. You can see,
the frame lidar is fixed now.

### Step 2.1 - Option 2 

* `Run Lidar first` with `NAV2 cycle` and `Fake Odom`
```
ros2 launch ldlidar_node ldlidar_with_mgr_tech.launch.py
```

* Then next, run our `SLAM` script as follow. Open new terminal and launch the following
```
ros2 launch ldlidar_node slam_launch_tech.launch.py
```

In new terminal, run `rviz2` and set the following configuration
```
Fixed Frame : map
LaserScan : /ldlidar_node/scan
Map : /map
```

### Step 2.2 - Option 2 : Run a modified version of SLAM with command

This step is quite similar to `Step 2.1`. Just follow this step

* `Run Lidar first` with `NAV2 cycle` and `Fake Odom`
```
ros2 launch ldlidar_node ldlidar_with_mgr_tech.launch.py
```

Open new terminal in your PC and run Command Line To launch Slam Tool Box. Here, we remap `/scan` topic to `/scan:=/ldlidar_node/scan` topic.
```
ros2 run slam_toolbox async_slam_toolbox_node --ros-args --params-file src/ldrobot-lidar-ros2/ldlidar_node/params/slam_toolbox.yaml --remap /scan:=/ldlidar_node/scan
```

In new terminal, run `rviz2` and set the following configuration
```
Fixed Frame : map
LaserScan : /ldlidar_node/scan
Map : /map
```
