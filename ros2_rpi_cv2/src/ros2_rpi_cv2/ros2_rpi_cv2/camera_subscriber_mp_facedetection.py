import rclpy
from rclpy.node import Node
import mediapipe as mp
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraMediaPipeSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_mediapipe_subscriber')
        topic_name = "/dkcar/camera"
        self.subscription = self.create_subscription(Image,topic_name, self.image_callback,20)
        self.subscription  
        self.cv_bridge = CvBridge()
        self.cv_window = cv2.namedWindow("Camera Image", cv2.WINDOW_NORMAL)

        self.mFace = mp.solutions.face_detection
        # face = mFace.FaceDetection()
        self.mpDraw = mp.solutions.drawing_utils

        self.pTime = 0
        self.cTime = 0
    
    def image_callback(self,msg):
        try:
            # Convert the ROS Image message to a NumPy array
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            with self.mFace.FaceDetection(min_detection_confidence=0.5) as face:
                cv_image.flags.writeable = True

                imgRGB = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                results = face.process(imgRGB)

                if results.detections:
                    for detections in results.detections:
                        for id, lm in enumerate(results.detections):
                            h, w, c = cv_image.shape
                            cv2.line(cv_image, (w//2, 0), (w//2, h), (0, 255, 0), 3)
                        self.mpDraw.draw_detection(cv_image, detections)
                
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

