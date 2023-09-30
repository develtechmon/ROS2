import rclpy
from rclpy.node import Node

## ros2 interface show sensor_msgs/msg/Range
from sensor_msgs.msg import Range
from lidar_vl53lox import Sonar

class LidarPublisher(Node):
    def __init(self):
        super().__init__('lidar_publisher')
        topic_name = "/dkcar/lidar"
        self.publishers_ = self.create_publisher(Range, topic_name, 5)
        
        message = Range()
        self._message = message

        self.scan()
        
        # timer_period = 0.5
        # self.timers = self.create_timer(timer_period, self.timer_callback)
        # self.i=0
    
    # def timer_callback(self):
    #     msg = String()
    #     msg.data = "Hello World"
    #     self.publishers_.publish(msg)
    
    def scan(self):
        message = Sonar()
        while True:
            range_cm = Sonar.read()
            self._message.range = range_cm * 0.01
            self.publishers_(self._message)
        
def main(args=None):
    rclpy.init(args=args)
    node=LidarPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()