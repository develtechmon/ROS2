import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/diff_cont/cmd_vel_unstamped', self.cmd_vel_callback, 10)
            #Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # Define GPIO pins for left and right wheels as class attributes
        self.left_motor_pins = {
            'enable': 25,
            'input1': 24,
            'input2': 23
        }

        self.right_motor_pins = {
            'enable': 17,
            'input1': 22,
            'input2': 27
        }

        # Disable GPIO warnings
        GPIO.setwarnings(False)

        # Set GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Set up GPIO pins
        for pin in self.left_motor_pins.values():
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.right_motor_pins.values():
            GPIO.setup(pin, GPIO.OUT)
        
        # Initialize PWM objects
        self.left_motor_pwm = GPIO.PWM(self.left_motor_pins['enable'], 100)
        self.right_motor_pwm = GPIO.PWM(self.right_motor_pins['enable'], 100)
        self.left_motor_pwm.start(0)
        self.right_motor_pwm.start(0)
        

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z
        
        wheel_radius = 0.3
        wheel_base = 0.11

        # Calculate motor speeds based on linear and angular velocity
        #left_speed  = (2*linear - (angular * wheel_base))/2*wheel_radius
        #right_speed = (2*linear + (angular * wheel_base))/2*wheel_radius
        left_speed  = (linear - angular) / 2
        right_speed = (linear + angular) / 2

        # Convert speed values to PWM duty cycle
        left_duty_cycle = abs(left_speed) * 100
        right_duty_cycle = abs(right_speed) * 100

        # Set motor direction based on speed sign
        left_direction = GPIO.HIGH if left_speed >= 0 else GPIO.LOW
        right_direction = GPIO.HIGH if right_speed >= 0 else GPIO.LOW

        # Set motor directions
        GPIO.output(self.left_motor_pins['input1'],  left_direction)
        GPIO.output(self.left_motor_pins['input2'], not left_direction) 
        GPIO.output(self.right_motor_pins['input1'], right_direction)
        GPIO.output(self.right_motor_pins['input2'], not right_direction)

        # Set motor speed via PWM
        self.left_motor_pwm.ChangeDutyCycle(left_duty_cycle)
        self.right_motor_pwm.ChangeDutyCycle(right_duty_cycle)

def main(args=None):
    rclpy.init(args=args)
    controller = MotorController()
    rclpy.spin(controller)

if __name__ == '__main__':
    main()
