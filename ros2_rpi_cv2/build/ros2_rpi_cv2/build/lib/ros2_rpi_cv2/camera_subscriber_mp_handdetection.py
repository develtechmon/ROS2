import rclpy
from rclpy.node import Node
import mediapipe as mp
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from ros2_rpi_cv2.HandTrackingModule import handDetector

class CameraMediaPipeSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_mediapipe_subscriber')
        topic_name = "/dkcar/camera"
        self.subscription = self.create_subscription(Image,topic_name, self.image_callback,10)
        self.subscription  
        self.cv_bridge = CvBridge()
        self.cv_window = cv2.namedWindow("Camera Image", cv2.WINDOW_NORMAL)

        self.pTime = 0
        self.cTime = 0

        self.detector = handDetector(detectionCon=0.5, maxHands=2)

    def image_callback(self,msg):
        try:
            # Convert the ROS Image message to a NumPy array
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            #imgRGB = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            #results = self.pose.process(imgRGB)

            height, width, centre = cv_image.shape
            hands,img = self.detector.findAllHands(cv_image)
            
            ## Draw Circle in the Middle Line
            cv2.circle(img, (width//2, height//2), 8, (0, 0, 255), cv2.FILLED)
            #cv2.rectangle(img, (0, height-24), (width,height), (0,0,0), -1)
            #cv2.rectangle(img, (width, 0), (0,60), (0,0,0), -1)
       
            cv2.imshow("Camera Image", cv_image)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Error processing image: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    camera_mediapipe_subscriber_node = CameraMediaPipeSubscriberNode()
    rclpy.spin(camera_mediapipe_subscriber_node)
    camera_mediapipe_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()    

