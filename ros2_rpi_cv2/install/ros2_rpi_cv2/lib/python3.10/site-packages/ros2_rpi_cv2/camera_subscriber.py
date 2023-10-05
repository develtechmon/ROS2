import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraSubscriberNode(Node):

    def __init__(self):
        super().__init__('camera_subscriber')
        topic_name = "/dkcar/camera"
        self.subscription = self.create_subscription(Image,topic_name, self.image_callback,10)
        self.subscription  
        self.cv_bridge = CvBridge()
        self.cv_window = cv2.namedWindow("Camera Image", cv2.WINDOW_NORMAL)

    def image_callback(self, msg):
        try:
            # Convert the ROS Image message to a NumPy array
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # Ensure the buffer size matches the image data size
            if cv_image.shape[0] != msg.height or cv_image.shape[1] != msg.width:
                self.get_logger().warn("Image dimensions do not match, skipping frame.")
                return

            #cv2.imshow("Camera Image", cv_image)
            print(cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Error processing image: {str(e)}")


def main(args=None):
    rclpy.init(args=args)
    camera_subscriber_node = CameraSubscriberNode()
    rclpy.spin(camera_subscriber_node)
    camera_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
