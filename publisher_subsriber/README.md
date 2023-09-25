## Getting Started

1. Create a workspace 
```
source /opt/ros/foxy/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

2. cd `ros2_ws` and run below command
```
colcon build
```

3. cd `ros2_ws/src` and we'll create a package here and run below command
```
ros2 pkg create --build-type ament_python <package_name>
```

4. cd `ros2_ws` and run this command
```
colcon build

. install/setup.bash
```

5. list the package `ros2 pkg list` and now you should able to `ros2_ws` recognize as one of the ros2 package