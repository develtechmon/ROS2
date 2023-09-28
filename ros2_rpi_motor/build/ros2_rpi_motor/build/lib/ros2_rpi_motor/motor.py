import pigpio
from time import sleep

pi = pigpio.pi()

M1A=17
M1B=18

pi.set_mode(M1A, pigpio.OUTPUT)
pi.set_mode(M1B, pigpio.OUTPUT)

def stop(speedLeft):
    pi.set_PWM_dutycycle(M1A,speedLeft)
    pi.set_PWM_dutycycle(M1B,speedLeft)

def forward(speedLeft):
    pi.set_PWM_dutycycle(M1A,speedLeft)
    pi.set_PWM_dutycycle(M1B,0)

def backward(speedLeft):
    pi.set_PWM_dutycycle(M1A,0)
    pi.set_PWM_dutycycle(M1B,speedLeft)

print("Forward..")
forward(200)

sleep(2)

print("Backward..")
backward(200)

sleep(2)

print("Stop..")
stop(0)
