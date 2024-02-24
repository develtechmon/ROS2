## Getting Started 

In this guide we're going to install update new `LD06` lidar to our `machine`. This is another revision from
the original repository.

## Step 1: Link
Refer to this link to get started
```
https://github.com/linorobot/ldlidar/tree/ros2
```

## Step 2: Git clone packages to our working directory as follow
```
mkdir ldlidar_ros2_ws_new
cd ldlidar_ros2_ws_new
mkdir src
cd src
git clone https://github.com/linorobot/ldlidar.git ldlidar
cd ..
sudo rosdep init
rosdep update && rosdep install --from-path src --ignore-src -y

colcon build

```

## Step 3: Launch our Package to work with `Odom` in RViz2
```
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=odom

To launch with specific port and lidar_link from urdf
ros2 launch ldlidar ldlidar.launch.py lidar_frame:=lidar_link serial_port:=/dev/ttyUSB1

```

## Step 4: Set Fix Port of our Lidar in RPI
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

## Step 5 : Above changes made on code above has been adjusted to work with `techdiffbot` REAL ROBOT

Here it consist new transform from URDF `(odom, base_footprint)` and `ldlidar_link`. To run this code
```
1.ros2 launch slam_toolbox online_async_launch.py slam_params_file:=src/techdiffbot/config/slam_toolbox.yaml use_sim_time:=false
2. ros2 launch ldlidar_stl_ros2 ld19.launch.py
3. ros2 launch techdiffbot launch_robot.launch.py
```
