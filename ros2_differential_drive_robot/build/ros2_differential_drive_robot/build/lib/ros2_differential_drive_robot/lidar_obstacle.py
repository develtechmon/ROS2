import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class LidarObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('lidar_obstacle')
        self.subscription = self.create_subscription(LaserScan,'/scan',  self.lidar_callback,10)

        self.publisher = self.create_publisher(Twist,'/cmd_vel',10)
        self.obstacle_detected = False

    def lidar_callback(self, msg):
        twist = Twist()
        if min(msg.ranges) < 0.8: 
            self.obstacle_detected = True
            
            # Obstacle detected, steer the robot
            twist.linear.x = 0.2
            twist.angular.z = 0.5

            print("obstacle detected")

        else:
            self.obstacle_detected = False

            # No obstacle detected, move forward
            twist.angular.z = 0.5
            
            print("no obstacle detected")

        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    lidar_obstacle_avoidance = LidarObstacleAvoidance()
    rclpy.spin(lidar_obstacle_avoidance)
    lidar_obstacle_avoidance.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()