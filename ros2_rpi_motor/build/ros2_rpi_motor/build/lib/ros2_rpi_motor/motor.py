import pigpio
from time import sleep

pi = pigpio.pi()

M1A=17
M1B=18

M2A=27
M2B=22

pi.set_mode(M1A, pigpio.OUTPUT)
pi.set_mode(M1B, pigpio.OUTPUT)

pi.set_mode(M2A, pigpio.OUTPUT)
pi.set_mode(M2B, pigpio.OUTPUT)

def stop(speedLeft):
    pi.set_PWM_dutycycle(M1A,speedLeft)
    pi.set_PWM_dutycycle(M1B,speedLeft)
    
    pi.set_PWM_dutycycle(M2A,speedLeft)
    pi.set_PWM_dutycycle(M2B,speedLeft)

def forward(speedLeft):
    pi.set_PWM_dutycycle(M1A,speedLeft)
    pi.set_PWM_dutycycle(M1B,0)

    pi.set_PWM_dutycycle(M2A,speedLeft)
    pi.set_PWM_dutycycle(M2B,0)

def backward(speedLeft):
    pi.set_PWM_dutycycle(M1A,0)
    pi.set_PWM_dutycycle(M1B,speedLeft)

    pi.set_PWM_dutycycle(M2A,0)
    pi.set_PWM_dutycycle(M2B,speedLeft)

print("Forward..")
forward(100)

sleep(1)

print("Backward..")
backward(100)

sleep(1)

print("Stop..")
stop(0)
