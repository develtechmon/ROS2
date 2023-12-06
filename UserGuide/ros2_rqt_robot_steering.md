# Getting Started

This is userguide on how to install `rqt_robot_steering` into our Environment. Using this package, you can monitor `angular velocity` and `rad/s` of our motor
from ROS2 simulation

See below guide

## Step 1: Run below command - To run `teleop keyboard`

Open `terminator` terminator and run following command to launch our `/cmd_vel` topic
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## Step 2: Open other new `terminator` terminal - To observe the `Twist` message.

Here we're going to observe `Twist` message published by `/cmd_vel`. Run following command
```
ros2 topic echo /cmd_vel
```

## Step 3: Install `rqt_robot_steering` package.

This is GUI approach to observe angular velocity `rad/s` and linear velocity `m/s`. Run following command to install this package
```
sudo apt-get install ros-humble-rqt-robot-steering
```
And run following command to `force discover` our installed package
```
ros2 run rqt_robot_steering rqt_robot_steering --force-discover
```

Next you can close this function and run `rqt` command as follow
```
rqt --force-discover
```
From the `interface` go to `Plugins` --> `Robot Tools` --> `Robot Steering`. You should see an interface popping out.
