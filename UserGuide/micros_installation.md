# Getting Started

This is step by step installation method on how to install `microros` into `Ubuntu` and `ESP32`. Any other micrcontroller should work fine.

## Step 1: Install Arduino and Setup ESP32 package

If you're using Ubuntu, you can download `Arduino` directly from the Store.
Once done then we'll install `ESP32` package as follow

* In your Arduino IDE, go to File> Preferences
* Enter following into `Additional Board Manager URL`
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
* Open the Boards Manager. Go to Tools > Board > Boards Manager
* Search for ESP32 and press install button for the `ESP32 by Espressif Systems` and select `v2.0.2` as required by `microros`

## Step 2: Download `microros2 arduino` package

* Go to micro_ros_arduino link as follow:
```
https://github.com/micro-ROS/micro_ros_arduino/tree/humble
```

* Download the file as `ZIP` package.
* From your `Arduino` Go to Sketch > Include Library > Add.ZIP library and browse for `micro_ros_arduino-humble.zip` package that we just downloaded.
* From `Example` list you should see new package that has been added such as `micro_ros_arduino`.

## Step 3: Upload our first `microros` file to `ESP32`
* Select `ESP32 Dev Module` and Port `dev/ttyUSB0` from the tools
* From `micro_ros_arduino` example list select `micro-ros_publisher` and `upload` this file to our `ESP32`.
* If you see `Connecting` from the terminal, please press `boot` button that enable the write function.

## Step 4: Install `micro-ROS-agent` into our `ROS2` package.

In order to speak with our `ESP32` and capture the `message` published by the `ESP32` we will need an agent to read this message.
Please follow below step

```
mkdir -p micro_ros/src
cd micro_ros/src/
git clone https://github.com/micro-ROS/micro-ROS-Agent.git -b humble

cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
. install/setup.bash 
```

## Step 5: Run `micro-ROS-agent` to capture Message published by `ESP32`

* To capture the topic or message, run following command. Remember, we're using `Serial Communication` instead of `Wifi` for this example
```
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 
```
* Open another `Terminal` and type below command. If not `topic` found, press `EN` button at `ESP32` to reset the communication again.
```
ros2 topic list
```
From `micro-ROS-agent` you should see the connection is `Successful`. To observe the message of our `topic`. Run following command
```
ros2 topic echo /micro_ros_arduino_node_publisher 
```
At this state, you should see `message` from `ESP32`. Good job !


