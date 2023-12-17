# Getting Started

This is userguide on how to add on `rviz plugin` that enable us to control the robot using `teleop` from
rviz

## Step 1: Create package name `teleop_gui`
```
mkdir -p teleop_gui/src
cd teleop_gui/src
```

## Step 2: Git Clone the `visualization` package
```
git clone -b ros2 https://github.com/ros-visualization/visualization_tutorials.git
```

## Step 3: Build the package
```
cd ..
colcon build --symlink-install 
```

## Step 4: Source the package
```
. install/setup.bash
```

## Step 5: Run rviz2 and add this panel
```
rviz2
```
From rviz2 select `Panels` and you should see under `rviz_plugin_tutorials` there is `Teleop`. 
You will use this package in your run.

## Step 6: From panel, you will need specify the `Output Topic` as follow
```
/diff_cont/cmd_vel_unstamped
```
