import rclpy
from rclpy.node import Node

## ros2 interface show sensor_msgs/msg/Range
#from sensor_msgs.msg import Range
from std_msgs.msg import Int32

#from ros2_rpi_lidar.module.lidar_vl53lox import Sonar
from ros2_rpi_lidar.distance import Sonar

class LidarPublisher(Node):
    def __init__(self):
        super().__init__('lidar_publisher')
        topic_name = "/dkcar/lidar"
        self.publishers_ = self.create_publisher(Int32, topic_name, 5)
        self.timer_ = self.create_timer(0.5, self.publish_ultrasonic_data)
        self.lidar = Sonar()
        
    
    def publish_ultrasonic_data(self):
        msg = Int32()
        #print(self.lidar.read)
        msg.data = self.lidar.read()
        self.publishers_.publish(msg)
        self.get_logger().info(f'Published Lidar Data: {msg.data}')

        
def main(args=None):
    rclpy.init(args=args)
    node=LidarPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
