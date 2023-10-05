import rclpy
'''
Without Timer
Blocking: Depending on the tasks within the loop, a non-timer-based approach can block
the main thread, making the node less responsive to other tasks and messages.

With Timer
Non-Blocking: Timers allow your node to perform tasks without blocking the main thread. 
This is particularly important in ROS 2 since it ensures that 
the node remains responsive to other tasks and messages.
'''

from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ros2_rpi_cv2.cv2_vision import cap

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        topic_name = "/dkcar/camera"
        self.publishers_ = self.create_publisher(Image, topic_name, 10)
        self.cv_bridge = CvBridge()
        self.cap = cap

    def publish_image(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                msg = self.cv_bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                self.publishers_.publish(msg)
                #self.get_logger().info(f'Published Camera Data: {msg.data}')
            else:
                break

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        node.publish_image()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
