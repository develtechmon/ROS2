## Getting Started 

In this guide we're going to install `LD06` lidar to our `machine`

## Step 1: Link
Refer to this link to get started
```
https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2
http://www.yahboom.net/study/LD06-DTOF
```

## Step 2: Check our Rosversion
```
rosversion -d
```

## Step 3: Create our `lidar` package and follow rest of the setup
```
mkdir -p ldlidar_ros2_ws/src
cd ldlidar_ros2_ws/src
```

## Step 4: Clone the package. This is only for `ROS2`
```
git clone https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2.git
```
 
## Step 5: Setup our `LD06` hardware. Please follow the schematic connection
![Alt text](image-1.png)
![Alt text](image-2.png)
![Alt text](image-3.png)

## Step 6: Find our Lidar `Serial`
```
ls /dev/ttyUSB*

You should see
/dev/ttyUSB0

and run below command
sudo chmod 777 /dev/ttyUSB0
```

## Step 6: Build our package
```
cd src/ldlidar_stl_ros2
cd launch
vi ld06.launch.py --> Here change the port_name: '/dev/ttyUSB0' based on detected serial. Save and exit the file

cd ../../..

colcon build
```

## Step 7: Source and Global source our `lidar` package
```
source install/setup.bash

We also can add our setup.bash to our ~jlukas/.bashrc script as follow. Save and quite and source our bashrc script again.
source /home/jlukas/Desktop/My_Project/ldlidar_ros2_ws/install/setup.bash
```
## Step 8: Launch `ld06 topic` and publish `/scan` data
```
ros2 launch ldlidar_stl_ros2 ld06.launch.py
```

## Step 9: Display our data in `rviz2`
```
ros2 topic list

You should see 
/scan

Open
rviz2

From rviz select Fixed Frame --> base_link
LaserScan --> Topic --> /scan
TF 
```

## Step 10: Set Fix Port of our Lidar in RPI
Type following command

```
/dev/serial/by-path/....<find port for our lidar>
```

Example as follow:
```
'port_name': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0'
```

Full Code
```

def generate_launch_description():
  # LDROBOT LiDAR publisher node
  ldlidar_node = Node(
      package='ldlidar_stl_ros2',
      executable='ldlidar_stl_ros2_node',
      name='LD19',
      output='screen',
      parameters=[
        {'product_name': 'LDLiDAR_LD19'},
        {'topic_name': 'scan'},
        #{'frame_id': 'base_laser'},  <--- Default from Factory
        {'frame_id': 'ldlidar_link'}, <--- Based on URDF
        {'port_name': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0'},
        #{'port_name': '/dev/ttyUSB1'},
        {'port_baudrate': 230400},
        {'laser_scan_dir': True},
        {'enable_angle_crop_func': False},
        {'angle_crop_min': 90.0},
        {'angle_crop_max': 270.0}
        #{'angle_crop_min': 135.0}, <---- New min
        #{'angle_crop_max': 225.0}  <---- New Max
      ]
  )

  # base_link to base_laser tf node
  base_link_to_laser_tf_node = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='base_link_to_base_laser_ld19',
    #arguments=['0','0','0.18','0','0','0','base_link','base_laser']  <--- Default from Factory
    arguments=['0','0','0','0','0','0','odom','base_footprint'] <---- Based on URDF
  )


  # Define LaunchDescription variable
  ld = LaunchDescription()
```

## Step 11 : Above changes made on code above has been adjusted to work with `techdiffbot` REAL ROBOT

Here it consist new transform from URDF `(odom, base_footprint)` and `ldlidar_link`. To run this code
```
1. ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/slam_toolbox.yaml use_sim_time:=false
2. ros2 launch ldlidar_stl_ros2 ld19.launch.py
3. ros2 launch techdiffbot launch_robot.launch.py
```
