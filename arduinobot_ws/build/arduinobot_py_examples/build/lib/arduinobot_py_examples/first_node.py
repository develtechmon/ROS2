import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FirstNode(Node):
    def __init__(self):
        super().__init__("first_node")
        self.counter = 0
        self.create_timer(1.0, self.timer_callback)
    
    def timer_callback(self):
        self.get_logger().info("Hello World " + str(self.counter))
        self.counter += 1

def main():
    rclpy.init()
    node = FirstNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()



