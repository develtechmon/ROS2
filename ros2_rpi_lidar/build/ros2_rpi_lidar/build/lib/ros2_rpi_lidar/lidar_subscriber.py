import rclpy
from rclpy.node import Node

## ros2 interface show sensor_msgs/msg/Range
#from sensor_msgs.msg import Range
from std_msgs.msg import Int32

class LidarSubscriber(Node):
    def __init__(self):
        super().__init__('lidar_subscriber')
        topic_name = "/dkcar/lidar"
        self.subscription = self.create_subscription(Int32,topic_name,self.lidar_listener_callback,5)
    
    def lidar_listener_callback(self,msg):
        msg = Int32()
        self.get_logger().info(f'Subscribed Lidar Data: {msg.data}')

        
def main(args=None):
    rclpy.init(args=args)
    node=LidarSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
