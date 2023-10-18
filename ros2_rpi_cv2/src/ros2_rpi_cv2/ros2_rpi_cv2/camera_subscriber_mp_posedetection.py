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
        self.subscription = self.create_subscription(Image,topic_name, self.image_callback,10)
        self.subscription  
        self.cv_bridge = CvBridge()
        self.cv_window = cv2.namedWindow("Camera Image", cv2.WINDOW_NORMAL)

        self.mPose = mp.solutions.pose
        self.pose = self.mPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils

        self.pTime = 0
        self.cTime = 0
    
    def image_callback(self,msg):
        try:
            # Convert the ROS Image message to a NumPy array
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            imgRGB = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            results = self.pose.process(imgRGB)

            if results.pose_landmarks:
                lmList = []
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h,w,c = cv_image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(id,lm)
                    lmList.append([id,cx,cy])
                    print(lmList[0], w,h)

                    cv2.circle(cv_image, (cx,cy),5, (255,0,0), 4)

                self.mpDraw.draw_landmarks(cv_image, results.pose_landmarks, self.mPose.POSE_CONNECTIONS)

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

