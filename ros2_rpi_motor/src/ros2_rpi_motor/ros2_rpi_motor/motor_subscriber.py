import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import pigpio
from time import sleep

class VelocitySubscriber(Node):
    def __init__(self):
        super().__init__('cmd_vel_subscriber')
        self.subscription = self.create_subscription(Twist,'cmd_vel',self.pwm_listener_callback,10)
        self.subscription  # prevent unused variable warning
        
        self.pi = pigpio.pi()
        
        self.M1A=17
        self.M1B=18
        
        self.pi.set_mode(self.M1A, pigpio.OUTPUT)
        self.pi.set_mode(self.M1B, pigpio.OUTPUT)

        self.pi.set_PWM_dutycycle(self.M1A, 0)
        self.pi.set_PWM_dutycycle(self.M1B, 0)

    def pwm_listener_callback(self, msg):
        right_wheel_vel = (msg.linear.x + msg.angular.z) / 2 
        left_wheel_vel  = (msg.linear.x - msg.angular.z) / 2

        print(right_wheel_vel, " / ", left_wheel_vel)
        
        if right_wheel_vel > 0:
            self.pi.set_PWM_dutycycle(self.M1A, 200)
            self.pi.set_PWM_dutycycle(self.M1B, 0)

        else:
            self.pi.set_PWM_dutycycle(self.M1A, 0)
            self.pi.set_PWM_dutycycle(self.M1B, 200)

        if right_wheel_vel == 0.0:
            self.pi.set_PWM_dutycycle(self.M1A, 0)
            self.pi.set_PWM_dutycycle(self.M1B, 0)

        #if left_wheel_vel > 0:
        #    self.pi.set_PWM_dutycycle(self.M1A, 200)
        #    self.pi.set_PWM_dutycycle(self.M1B, 0)

def main(args=None):
    rclpy.init(args=args)
    node = VelocitySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
            
