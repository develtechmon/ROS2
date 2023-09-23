# Getting Started

Create Workspace
1. mkdir -p arduinorobot_ws/src
2. cd arduinorobot_ws
3. run command `colcon build`. This will generate build, install and log directories

Functions as follow
```
src - where our project will be
install - where our setup file will be 
log - nothing just a log
```

4. Next `cd` to `src` and we'll create our package as follow. select `ament_python` for `python` or `ament_cmake` for `c++`
```
ros2 pkg create --build-type ament_python arduinobot_py_example
ros2 pkg create --build-type ament_cmake arduinobot_cpp_example
```

5. Next run `colcon build` again to compile all the files

6. By default, `ros2` wont recognize our package, therefore we need to `source` the `bash` file to source this as follow
```
. install/setup.bash
```

7. Then you will see your directory `arduinobot_py_example` and `arduinobot_cpp_example` will be part of the package. Run as follow to see this package

```
ros2 pkg list
```

8. Run below command to avoid building again everytime
```
colcon build --symlink-install
```

## Command 
1. Use this command if you want to publish your data from terminal as follow:
```
ros2 topic pub /chatter std_msgs/msg/String "data: 'Hello Motherfucker !'"

chatter - referring to topic
std_msgs/msg/String - standard data messages obtain from auto completion
```

2. This will publish data to `chatter` topic and the `simple_subscriber` will obtain this
messages and display it