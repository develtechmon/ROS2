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
/*
PWM Pin In Arduino Nano
D3 // Interrupt
D5
D6
D9
D10
D11
*/
#ifdef L298_MOTOR_DRIVER
  #define LEFT_MOTOR_ENABLE   13 // 
  #define RIGHT_MOTOR_ENABLE  11 // 
  #define RIGHT_MOTOR_BACKWARD 5 // in4 // Motor B
  #define RIGHT_MOTOR_FORWARD  9 // in3 // Motor B
  #define LEFT_MOTOR_BACKWARD  6 // in2 // Motor A
  #define LEFT_MOTOR_FORWARD  10 // in1 // Motor A 

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


## Step 4 : Open your `RPI` either using `SSH` or Directly to `RPI monitor`.

Once you done, please connect your `Arduino USB` to `RPI USB Port`. Once you connect, please install following `Serial` package
```
sudo apt-get install python3-serial
```

Then install following `CH340` Library

Please refer to this link
* https://www.chippiko.com/ch340-dev-ttyusb-not-showing
```
sudo apt install gcc-12
git clone https://github.com/juliagoda/CH341SER.git

cd CH341SER
make
sudo make load
```

Next add Group using below command. This is to enable access to serial.
```
sudo adduser $USER dialout

or

sudo usermod -a -G dialout jlukas <-- To allow access to /dev/ttyUSB*
```

Once you done, reboot the `RPI`.

After reboot, then you should see `/dev/ttyUSB0` if you run below command
```
ls /dev/ttyUSB0
```
## Step 5 : Run `pyserial-miniterm`

Open your terminal and run `pyserial-miniterm` command as follow.
```
pyserial-miniterm -e /dev/ttyUSB0 57600
```
This command will invoke the 
connection with `Arduino Nano` similarly as `serial monitor` that we did in `Arduino IDE`.
But here, we're using `Terminal` directly.

You can use similar `command` as in `README.md` as mentioned intially.

## Step 6: Run `serial motor demo`
In your `RPI` clone following packages and follow the step
```
mkdir -p ros2_serial_motor_demo/src
cd ros2_serial_motor_demo/src

git clone https://github.com/joshnewans/serial_motor_demo.git
cd ..
colcon build --symlink-install

. install/setup.bash
```
Then run this command in your `rpi`
```
ros2 run serial_motor_demo driver --ros-args -p serial_port:=/dev/ttyUSB1 -p baud_rate:=57600 -p loop_rate:=30 -p encoder_cpr:=1320
```

And in your development computer, clone above package as well and follow same step.

To control motor, run following command in your development computer
```
ros2 run serial_motor_demo gui
```




