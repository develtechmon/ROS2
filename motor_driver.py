import RPi.GPIO as GPIO          
from time import sleep

motor_in1 = 24
motor_in2 = 23
en_0 = 25

motor_in3 = 22
motor_in4 = 27
en_1 = 17

# Disable GPIO warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(motor_in1,GPIO.OUT)
GPIO.setup(motor_in2,GPIO.OUT)
GPIO.setup(en_0,GPIO.OUT)

GPIO.setup(motor_in3,GPIO.OUT)
GPIO.setup(motor_in4,GPIO.OUT)
GPIO.setup(en_1,GPIO.OUT)

GPIO.output(motor_in1,GPIO.LOW)
GPIO.output(motor_in2,GPIO.LOW)
GPIO.output(motor_in3,GPIO.LOW)
GPIO.output(motor_in4,GPIO.LOW)

pwm1=GPIO.PWM(en_0,1000)
pwm2=GPIO.PWM(en_1,1000)

pwm1.start(50)
pwm2.start(50)

# Function to move the motor forward
def move_forward():
    GPIO.output(motor_in1, GPIO.HIGH)
    GPIO.output(motor_in2, GPIO.LOW)

    GPIO.output(motor_in3, GPIO.HIGH)
    GPIO.output(motor_in4, GPIO.LOW)

# Function to move the motor backward
def move_backward():
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.HIGH)

    GPIO.output(motor_in3, GPIO.LOW)
    GPIO.output(motor_in4, GPIO.HIGH)

# Function to stop the motor
def stop_motor():
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.LOW)

    GPIO.output(motor_in3, GPIO.LOW)
    GPIO.output(motor_in4, GPIO.LOW)

try:
    while True:
        # Move the motor forward for 2 seconds
        move_forward()
        sleep(2)

        # Move the motor backward for 2 seconds
        move_backward()
        sleep(2)

        # Stop the motor for 2 seconds
        stop_motor()
        sleep(2)

except KeyboardInterrupt:
    pass

# Clean up the GPIO settings and stop PWM
pwm1.stop()
pwm2.stop()
GPIO.cleanup()
