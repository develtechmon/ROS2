import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vl53lox import *
class LidarPublisher(Node):
    def __init(self):
        super().__init__('lidar_publisher')
        topic_name = "/dkcar/lidar"
        self.publishers_ = self.create_publisher(String, topic_name, 10)
        timer_period = 0.5
        self.timers = self.create_timer(timer_period, self.timer_callback)
        self.i=0
    
    def timer_callback(self):
        msg = String()
        msg.data = "Hello World"
        self.publishers_.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    node=LidarPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()