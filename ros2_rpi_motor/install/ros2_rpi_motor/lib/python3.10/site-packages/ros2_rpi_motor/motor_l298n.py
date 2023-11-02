import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.setup_gpio_pins()

    def setup_gpio_pins(self):
        GPIO.setmode(GPIO.BCM)

        # Define GPIO pins for left and right wheels
        left_motor_pins = {
            'enable': 17,
            'input1': 22,
            'input2': 27
        }

        right_motor_pins = {
            'enable': 25,
            'input1': 24,
            'input2': 23
        }

        for pin in left_motor_pins.values():
            GPIO.setup(pin, GPIO.OUT)

        for pin in right_motor_pins.values():
            GPIO.setup(pin, GPIO.OUT)

        # Set PWM for the enable pins
        self.left_motor_pwm = GPIO.PWM(left_motor_pins['enable'], 100)
        self.right_motor_pwm = GPIO.PWM(right_motor_pins['enable'], 100)
        self.left_motor_pwm.start(0)
        self.right_motor_pwm.start(0)

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        # Calculate motor speeds based on linear and angular velocity
        left_speed = linear - angular
        right_speed = linear + angular

        # Convert speed values to PWM duty cycle
        left_duty_cycle = abs(left_speed) * 100
        right_duty_cycle = abs(right_speed) * 100

        # Set motor direction based on speed sign
        left_direction = GPIO.HIGH if left_speed >= 0 else GPIO.LOW
        right_direction = GPIO.HIGH if right_speed >= 0 else GPIO.LOW

        # Set motor directions
        GPIO.output(self.left_motor_pins['input1'], left_direction)
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


