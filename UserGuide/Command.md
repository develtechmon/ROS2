# Getting started

- ros2 launch gazebo_ros gazebo.launch.py
- ros2 launch src/ros2_differential_drive_robot/launch/rviz2.launch.py 
- ros2 launch src/ros2_differential_drive_robot/launch/rsp.launch.py
- ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity lukebot
- ros2 topic echo /scan 
- ros2 run joint_state_publisher_gui joint_state_publisher_gui
- ros2 run teleop_twist_keyboard teleop_twist_keyboard 

## To launch the `saved world`
- ros2 launch ros2_differential_drive_robot gazebo.sim.launch.py world:=/src/ros2_differential_drive_robot/worlds/obstacle_avoidance.world
