# Getting started

This userguide show on how to setup `ros2 control` with `Arduino Nano` that i'm using
in this setup. Refer to setup below

## Step 1 : Clone the directory
```
cd /home/jlukas/Desktop
git clone https://github.com/joshnewans/ros_arduino_bridge.git
```

## Step 2 : Modify the pin as follow

Open your `Arduino IDE` and apply fooling configuration

`motor_driver.h`
```
/***************************************************************
   Motor driver function definitions - by James Nugen
   *************************************************************/

#ifdef L298_MOTOR_DRIVER
  #define RIGHT_MOTOR_BACKWARD 12 //5 <---- (5 original, 12 is modify)
  #define LEFT_MOTOR_BACKWARD  6
  #define RIGHT_MOTOR_FORWARD  9
  #define LEFT_MOTOR_FORWARD   10
  #define RIGHT_MOTOR_ENABLE 5 //12 <---- (12 original, 5 is modify)
  #define LEFT_MOTOR_ENABLE 11 //13 <---- (13 original, 11 is modify)
#endif

void initMotorController();
void setMotorSpeed(int i, int spd);
void setMotorSpeeds(int leftSpeed, int rightSpeed);

```

Then upload the program into your `Arduino Nano`. Please ensure right port is selected.

## Step 3 : Open `Arduino IDE` serial

From Serial monitor refer to following keyword to play around with motor. Please refer to `README.md` for 
details.

The main commands to know are

* e - Motor responds with current encoder counts for each motor
* r - Reset encoder values
* o <PWM1> <PWM2> - Set the raw PWM speed of each motor (-255 to 255)
* m <Spd1> <Spd2> - Set the closed-loop speed of each motor in counts per loop (Default loop rate is 30, so (counts per sec)/30
* p <Kp> <Kd> <Ki> <Ko> - Update the PID parameters
