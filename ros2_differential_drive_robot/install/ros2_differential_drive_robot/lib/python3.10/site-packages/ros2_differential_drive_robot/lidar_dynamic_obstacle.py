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
        
        self.critical_distance = 0.7
        self.max_angular_speed = 0.15
        self.max_linear_speed = 0.5
        self.kp = 3.0

    def lidar_callback(self,msg):
        min_distance = min(msg.ranges)
        print(min_distance)
        if min_distance < 1:
            print("obstacle detected")
            error = min_distance - self.critical_distance
            #forward_speed  = self.kp * error
            angular_speed  = self.kp * error
            
            angular_speed  = min(max(angular_speed,  -self.max_angular_speed), self.max_angular_speed)
            #forward_speed  = min(max(forward_speed , -self.max_linear_speed),  self.max_linear_speed)

            #self.twist.angular.z = forward_speed
            self.twist.linear.x = angular_speed
        
        else:
            print("no obstacle detected")
            self.twist.angular.z = -1.0
            self.twist.linear.x = 0.0
        self.publisher.publish(self.twist)
        
def main(args=None):
    rclpy.init(args=args)
    lidar_obstacle_avoidance = LidarObstacleAvoidanceSteer()
    rclpy.spin(lidar_obstacle_avoidance)
    lidar_obstacle_avoidance.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()