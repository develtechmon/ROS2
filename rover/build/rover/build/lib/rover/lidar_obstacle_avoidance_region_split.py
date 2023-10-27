import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
from time import sleep

class LidarObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('lidar_obstacle')
        
        # Publisher
        self.publisher = self.create_publisher(Twist,'/cmd_vel',40)
        
        # Subscriber
        self.subscription = self.create_subscription(LaserScan,'/scan', self.get_scan_values,40)

        # Periodic Publisher call
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.send_cmd_vel)

        # Default Velocity Value        
        self.linear_vel = -0.5
        
        # Create dictionary for laser scan
        self.regions = {'right':[], 'mid':[], 'left':[]}
        
        # Create message object for velocity
        self.twist =Twist()
        
    def get_scan_values(self,msg):
        #min_distance = min(msg.ranges)

        self.regions = {
        'right': int(min(min(msg.ranges[0:120]),   100)),
        'mid':   int(min(min(msg.ranges[120:240]), 100)),
        'left':  int(min(min(msg.ranges[240:360]), 100)),    
        }
        
        print("left", self.regions['left']," / ", "medium", self.regions['mid']," / ", "right" , self.regions['right'])

        #self.publisher.publish(self.twist)
        
    def send_cmd_vel(self):
        self.twist.linear.x = self.linear_vel

        try:
            if int(self.regions['left'] > 2  and self.regions['mid'] > 2  and self.regions['right'] > 2 ):
                self.twist.angular.z=0.0 # condition in which area is total clear
                print("forward")
            
            elif int(self.regions['left'] > 2 and self.regions['mid'] > 2  and self.regions['right'] < 2 ):
                self.twist.angular.z= 1.57# object on right,taking  left 
                print("left")
                
            elif int(self.regions['left'] < 2 and self.regions['mid'] > 2  and self.regions['right'] > 2 ):
                self.twist.angular.z= -1.57 #object  on left, taking  right
                print("right")          
                
            # elif int(self.regions['left'] < 2 and self.regions['mid'] < 2  and self.regions['right'] < 2 ):
            #     self.twist.angular.z= 0.5 #-3.14# object ahead take full turn
            #     self.twist.linear.x = 0.5
            #     print("reverse")
                
            else:## lThis code is not completed ->  you have  to add more conditions  ot make it robust
                print("some other conditions are required to be programmed")
        except:
            pass
 
        self.publisher.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    lidar_obstacle_avoidance = LidarObstacleAvoidance()
    rclpy.spin(lidar_obstacle_avoidance)
    lidar_obstacle_avoidance.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()