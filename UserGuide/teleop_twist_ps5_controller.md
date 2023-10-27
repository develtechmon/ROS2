## Getting Started

To list all the available package. Run below command
```
ros2 pkg list
```

From the package list, you can find `teleop_twist_joy` package. 

In this example, we're going to read input from `Joystick` using his package.

Here i launch the package that read the `ps5 joystick` as follow 

```
ros2 launch teleop_twist_joy teleop-launch.py 
```
By default, input reading won't successful because this package didn't support this `joystick`. To resolve this, we can use this command to enable us to read `ps5 joystick` input
```
ros2 param set /teleop_twist_joy_node require_enable_button false
```

At this example, we haven't yet create a `subscriber`, therefore to listen to the `topic` we can 
run below command.

This command is used to listen to above command
```
ros2 topic echo /cmd_vel
```

