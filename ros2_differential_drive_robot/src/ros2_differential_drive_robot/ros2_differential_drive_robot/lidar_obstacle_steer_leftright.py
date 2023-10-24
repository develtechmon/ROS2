import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np


class LidarObstacleAvoidanceSteer(Node):
    def __init__(self):
        super().__init__('lidar_obstacle')
        self.subscription = self.create_subscription(LaserScan,'/scan',  self.lidar_callback,10)

        self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
        self.obstacle_detected = False

    def lidar_callback(self,msg):
        ranges = msg.ranges
        min_range = min(ranges)
        if min_range < 0.8:
            self.obstacle_detected = True
            min_index = np.argmin(ranges)

            # Calculate the angle of the closest obstacle relative to the front of the robot
            angle = msg.angle_min + min_index * msg.angle_increment
            print(angle)
            self.steer_robot(angle)

        else:
            # No obstacle detected, move Forward
            self.obstacle_detected = False
            self.steer_robot(0.0) # Steer forward

    def steer_robot(self, angle):
        twist = Twist()
        if self.obstacle_detected:
            # Obstacle detected, steer the robot
            if angle > 0.0:
                # Obstacle on the right, steer right and move forward
                twist.angular.z = 0.5  # Adjust the steering angular velocity as needed
                twist.linear.x = 0.2  # Adjust the forward velocity as needed
            else:
                # Obstacle on the left, steer left and move forward
                twist.angular.z = -0.5  # Adjust the steering angular velocity as needed
                twist.linear.x = 0.2  # Adjust the forward velocity as needed
        else:
            # No obstacle detected, move forward
            twist.angular.z = 0.5
            #twist.linear.x = 0.2  # Adjust the forward velocity as needed
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    lidar_obstacle_avoidance = LidarObstacleAvoidanceSteer()
    rclpy.spin(lidar_obstacle_avoidance)
    lidar_obstacle_avoidance.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()