import rclpy
from rclpy.node import Node

## ros2 interface show sensor_msgs/msg/Range
from sensor_msgs.msg import Image

from scripts.cv2_vision import cap

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        topic_name = "/dkcar/camera"
        self.publishers_ = self.create_publisher(Image, topic_name, 10)
        self.timer_ = self.create_timer(0.1, self.publish_lidar_data)
        self.cap = cap
        
    def publish_lidar_data(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                msg = Image()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.data = frame.tobytes()
                msg.width = frame.shape[1]
                msg.height = frame.shape[0]
                msg.encoding = 'bgr8'
                msg.step = len(msg.data)
                self.publishers_.publish(msg)

                self.get_logger().info(f'Published Camera Data: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node=CameraPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
