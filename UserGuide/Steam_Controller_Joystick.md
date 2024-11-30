```
sudo apt-get install joystick jstest-gtk evtest
sudo apt install ros-humble-joy-tester
```

To scan the driver
```
sudo evtest
```
Then select the device event number [0-5]. In this case, i'm going to select `5`.

Then `play` your `steam controller`. You should see the changes instantly in the terminal.

Next type below command. This command will launch `Joystick Preferences` and select the `icon`. You will see all the `Axis` that relate to your controller appear.
```
jstest-gtk
```

Next type below command to determine the `Joystick ID`
```
ros2 run joy joy_enumerate_devices
```
You will following result
```
0: Wireless Steam Controller
```

To connect to our `Controller` run following command. This will publich `/joy`topic.
```
ros2 run joy joy_node
```
To listen to the `/joy` topic run following command
```
ros2 topic echo /joy
``` 

You will see `1` or `0` result from the controller.

Next run below command to see all the `parameter` list
```
ros2 param list
```

Next run below command. This command will open new `GUI` window of `controller` output.
```
ros2 run joy_tester test_joy
```


# Additional Info.

If `controller` not detected and not have non consistent connectivity behavior. Please run following command to resolve this use
```
sudo usermod -aG input $USER
sudo chmod a+rw /dev/input/event1
```
