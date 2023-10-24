import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
from time import sleep

class LidarObstacleAvoidanceSteer(Node):
    def __init__(self):
        super().__init__('lidar_obstacle')
        self.subscription = self.create_subscription(LaserScan,'/scan',  self.lidar_callback,10)
        self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
        self.obstacle_detected = False
        self.twist = Twist()

    def lidar_callback(self,msg):
        min_distance = min(msg.ranges)
        critical_distance = 0.5
        max_angular_speed = 0.05
        max_linear_speed = 1.0
        min_linear_speed = 0.3

        if min_distance > critical_distance:
            print("no obstacle detected")
            self.twist.angular.z = max_linear_speed
            self.twist.linear.x = 0.0
        else:
            print("obstacle detected")
            self.twist.angular.z = min_linear_speed
            self.twist.linear.x = max_angular_speed
        self.publisher.publish(self.twist)

    # def lidar_callback(self,msg):
    #     ranges = msg.ranges
    #     min_range = min(ranges)
    #     if min_range < 0.5:
    #         self.obstacle_detected = True
    #         min_index = np.argmin(ranges)

    #         # Calculate the angle of the closest obstacle relative to the front of the robot
    #         angle = msg.angle_min + min_index * msg.angle_increment
    #         print(angle)
    #         self.steer_robot(angle)

    #     else:
    #         # No obstacle detected, move Forward
    #         self.obstacle_detected = False
    #         self.steer_robot(0.0) # Steer forward

    # def steer_robot(self, angle):
    #     if self.obstacle_detected:
    #         print("obstacle detected")
    #         # Obstacle detected, steer the robot
    #         if angle > 0.0:
    #             # Obstacle on the right, steer right and move forward
    #             twist.angular.z = 0.5  # Adjust the steering angular velocity as needed
    #             twist.linear.x = 0.1  # Adjust the forward velocity as needed
    #         else:
    #             # Obstacle on the left, steer left and move forward
    #             twist.angular.z = -0.5  # Adjust the steering angular velocity as needed
    #             twist.linear.x = 0.1  # Adjust the forward velocity as needed

    #     elif self.obstacle_detected == False:
    #         print("no obstacle detected")
    #         # No obstacle detected, move forward
    #         twist.angular.z = 0.5
    #         #twist.linear.x = 0.2  # Adjust the forward velocity as needed
    #     self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    lidar_obstacle_avoidance = LidarObstacleAvoidanceSteer()
    rclpy.spin(lidar_obstacle_avoidance)
    lidar_obstacle_avoidance.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()