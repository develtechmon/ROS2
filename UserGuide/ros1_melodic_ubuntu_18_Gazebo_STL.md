Ubuntu 18.04.4 LTS
Release 18.04
Codename Bionic

# Big Screen issues in v18 Ubuntu
```
sudo apt-get update -y && sudo apt-get ugprade -y
sudo apt-get install open-vm-tools -y
sudo apt install virtualbox-guest-additions-iso -y

sudo mkdir -p /mnt/cdrom
sudo mount /usr/share/virtualbox/VBoxLinuxAdditions.iso /mnt/cdrom
cd /mnt/cdrom
ll
sudo ./VBoxLinuxAdditions.run
sudo reboot 
```


# SITL Installation

1. Install Python 2.7 Pip package
```
sudo apt-get update
sudo apt-get upgrade

curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py -k
sudo python get-pip.py
pip --version
```

Once completed run velow command to to determine if installed pip is refer to python 2.7 using below command
```
whereis pip
```

2. Install python 3 pip
```
sudo apt-get update
curl https://bootstrap.pypa.io/pip/3.6/get-pip.py --output get-pip_3_6.py
sudo python get-pip_3_6.py
pip --version

or

Use this if above doesnt work

sudo apt-get update
sudo apt install python3-pip

```
Once completed run python to check if pip installed pip is refer to python 3.6 using below command
```
whereis pip
```


3. Install Ardupilot and relevant packages
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-wxgtk4.0 -y <--- Install this if you sim_vehicle can'f find map and console
sudo apt-get install git
sudo pip install pexpect
sudo pip install future
sudo pip install pyserial
sudo pip install dronekit
sudo pip install MAVProxy
sudo pip install keyboard
sudo pip install pymavlink==2.4.37 <===== important to avoid def init(self, buf: Optional[Sequence[int]] = None) -> None: Error SyntaxError: invalid syntax

git config --global http.sslverify false
git clone https://github.com/ArduPilot/ardupilot

cd ardupilot
git submodule update --init --recursive

./Tools/environment_install/install-prereqs-ubuntu.sh -y
```

4. Load the `profile`
```
. ~/.profile (Space in between . and ~ - reload this profile if sim_vehicle not found)
```
5. Start the simulator
```
cd ardupilot/Arducopter
```

6. First run to write the virtual EEPROM. After default parameters are loaded then can start simulator normally
```
sim_vehicle.py -w
```

# There will be a time you will encounter `waf fatal` during compilation after running `sim_vehicle -w`.
This is due to developer commit cause a problem. To solve this, you can visit `ardupilot github` page 
and read their commit `id`. In my case i `checkout` to specific `id`
```
cd ardupilot
git checkout 87435473b547a8096234f2ff473278de2fae0a00
git reset --hard 87435473b547a8096234f2ff473278de2fae0a00
```

This action will revert to that `id` change before the update. Sometime developer will cause mistake.
If you encounter error `Checking for python version >= 3.6.9 : 2.7.17
The python version is too old, expecting (3, 6, 9)`.

You can solve this by go to
```
Go to ./ardupilot/modules/waf

and in the file waf-light

change first line: #!/usr/bin/env python to #!/usr/bin/env python3
```

Then run this command again
```
sim_vehicle.py -w
```

See this link for reference
```
https://discuss.ardupilot.org/t/arduplane-sitl-build-failing-on-ubuntu-18-04/55804/12
```

# Gazebo 9
```
1. sudo apt install python-opencv=3.2.0+dfsg-4ubuntu0.1
```

```
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt update
sudo apt install gazebo9 libgazebo9-dev
gazebo --verbose

sudo vi .ignition/fuel/config.yaml
Replace name url: https://fuel.ignitionrobotics.org
save and quit
```

```
3. git clone https://github.com/dronedojo/ardupilot_gazebo
cd ardupilot_gazebo
mkdir build
cd build
sudo apt install cmake
cmake ..
make -j4
sudo make install
```
```
sudo vi ~jlukas/.bashrc and add following line
export GAZEBO_RESOURCE_PATH="/home/jlukas/ardupilot_gazebo":"/home/jlukas/ardupilot_gazebo/worlds":"/usr/share/gazebo-9"
export GAZEBO_MODEL_PATH="/home/jlukas/ardupilot_gazebo/models":"/usr/share/gazebo-9/models"

source /usr/share/gazebo-9/setup.sh
```

Then we need to edit aboive setup.sh file
```
sudo vi  /usr/share/gazebo-9/setup.sh
Please remove 
export GAZEBO_RESOURCE_PATH
export GAZEBO_MODEL_PATH

save and quit
```

# Install ros2 melodic
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl

If you can't add the key, you can run below command to run it manually
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654

If you can add the key, you can run below command to ping the server
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update
sudo apt install ros-melodic-desktop-full

Add this to .bashrc:
source /opt/ros/melodic/setup.bash
sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
sudo apt install python-rosdep
sudo rosdep init
rosdep update

sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
```

Next we're going to fly our `drone` in Gazebo. Run following command in new terminal
```
gazebo iris_arducopter_runaway.world
gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_runway.world

cd ardupilot/ArduCopter
../Tools/autotest/sim_vehicle.py -f gazebo-iris --console --map

or

sim_vehicle.py -v ArduCopter -f gazebo-iris --console
```

To invoke `mavproxy` terminal
```
mavproxy.py --master=127.0.0.1:14550
```

If you encounter error `VMware: vmw_ioctl_command error Invalid argument`. Run following command to remove
this error

1. Downgrade `GL_VERSION` from 3.3 to 2.1. This method will work better and Gazebo performance also good
```
echo "export SVGA_VGPU10=0" >> ~/.bashrc
```

2. Disable Graphic Acceleration in VMWARE. This method OK but will reduce 3D performance in Gazebo
```
Untick Accelerate 3D Graphics.
```
Check below link for good reference
```
https://robocademy.com/2020/05/02/solved-opengl-issues-with-gazebo-and-vmware/
```

# Ros programming

# To start `Gazebo` Simulation using ros
First we have to modify launch file in `gazebo` as follow
```
roscd gazebo_ros --> to list down the package inside gazebo_ros
```

and edit an copy new `empty_world` to `iris_world` and change `world name`
```
cd launch
sudo cp -r empty_world.launch iris_world.launch

sudo gedit iris_world.launch

inside this launch file set the parameter of "world_name" default="aruco_landing.world"
```

To launch our launch file. This will launch our `aruco_landing.world`
```
roslaunch gazebo_ros iris_world.launch
```

Check Topic and Visualization
```
rostopic list --> to check topic publish by drone
rostopic hz /camera/color/image_raw --> To check the rate of this topic publish
```

Visualization
```
rqt --> To see the relationship list
```

From `rqt` go to following tab
```
Visualization --> Image View --> /camera/color/image_raw
```

Create our first `ros` project
```
mkdir catkin_ws
cd catkin_ws
mkdir src
catkin make
```

Then export our `setup.bash` into our `.cshrc` script
```
echo "source /home/jlukas/Desktop/My_Project/catkin_ws/devel/setup.sh" >> ~jlukas/.bashrc 
```

To check if the path has been exported
```
tail -2 ~jlukas/.bashrc
```

Then we will need to create a ros package inside `src`. Package is a collection of our `node`

ROS1
```
cd src
catkin_create_pkg example_pkg rospy roscpp
```

ROS2
```
ros2 pkg create --build-type ament_python example_pkg
cd ..
colcon build
```

Once you done create the package then follow below step
```
cd src/example_pkg
mkdir scripts
mkdir example_publisher.py
chmod +x

mkdir example_subscriber.py
chmod +x
```
And Copy following `Publisher Script`
```
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def publisher():
    # Create a ros publisher
    pub = rospy.Publisher("ExampleTopic", String, queue_size=10)

    # Initialize our Node
    rospy.init_node("exampleNode", anonymous=False)

    rate = rospy.Rate(10) #Hz - run ten time per second
     
    while not rospy.is_shutdown():
        string_data = "Hello Drone Lukas"
        pub.publish(string_data)
        rate.sleep()

if __name__ == "__main__":
    publisher()
```

And Copy following `Subscriber Script`
```
#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(msg):
    string_data = msg.data
    print(string_data)

def subscriber():
    # Initialize our Node
    rospy.init_node("exampleNode_subs", anonymous=False)

    # Create a ros subscriber to ExampleTopic
    rospy.Subscriber('ExampleTopic', String, callback)
    rospy.spin()

if __name__ == "__main__":
    subscriber()

```

Once you done then follow below step to compile our `updated` package
```
cd ../..
catkin_make
```

Open new terminal and run `roscore` command to start `ros`
```
roscore
```

and run our code above as follow
```
rosrun example_pkg example_publisher.py
```

and observe the public topic 
```
rostopic list

You will see --> /ExampleTopic 
```

To check all available `node`
```
rosnode list

You will see /exampleNode 
```

To check publish rate of our `Topic`
```
rostopic hz /ExampleTopic

Here you should average rate is ~ 10Hz which match to our publish rate
```

To check `topic` message type
```
rostopic list

rostopic info exampleTopic --> This will show std_msgs/String
```

To check `topic` message data type
```
rosmsg show std_msgs/String --> This will shouw string data
```

In short
```
jlukas@ubuntu:~$ rostopic list
/ExampleTopic <---- The topic 
/rosout
/rosout_agg

jlukas@ubuntu:~$ rostopic info /ExampleTopic
Type: std_msgs/String <----- The message

Publishers: 
 * /exampleNode_pub (http://ubuntu:44287/)

Subscribers: None

jlukas@ubuntu:~$ rosmsg show std_msgs/String
string data <--------- Message type
```

# For rest of the script file. You can find it at `drone dojo`
We will use this package later to work with our `aruco drone` project.
```
https://github.com/dronedojo/pidronescripts.git
```

# Clone `ROS numpy` into `src` directory
Next we're going to `Git Clone` package. This tools is needed to convert
ROS messages and convert it into Numpy Array. We will later subscribe to below topic
from Gazebo and deserialize it into numpy array using the package

Package to clone
```
cd /catkin_ws/src/
git clone https://github.com/eric-wieser/ros_numpy.git

cd ../..
```

# Write our First `track_aruco.py` script.

Follow by step accordingly. We're going to create `gazebo_drone` package
```
cd src/
catkin_create_pkg gazebo_drone rospy roscpp

cd gazebo_drone
mkdir scripts
touch track_aruco.py
cd ..

catkin_make
```

Run our `Gazebo` and `sim_vehicle` file to obtain below parameters
Gazebo
```
roslaunch gazebo_ros iris_world.launch
```

sim_vehicle
```
sim_vehicle.py -v ArduCopter -f gazebo-iris --console --map
```
set mod to `GUIDED` and then `takeoff for 2meter`.

We'll use below `parameter` that will be adopted into our `script file` later
```
rostopic list
    ---> /camera/color/image_raw
```

Message Type
```
rostopic info /camera/color/image_raw
    ---> Type: sensor_msgs/Image
```

Message Data
```
rosmsg show sensor_msgs/Image
You wll find unint8[] data which later we will use to deserialize using ros numpy
```

Now to look up for camera intrinsic for Gazebo

In script we will need to supply this parameters
```
dist_coeff = []
camera_matrix = [[],[],[]]
```

To find this parameters you can run
```
rostopic echo /camera/color/camera_info
```
This will show below result
```
header: 
  seq: 129
  stamp: 
    secs: 208
    nsecs: 746000000
  frame_id: "camera_link"
height: 720
width: 1280
distortion_model: "plumb_bob"
D: [0.0, 0.0, 0.0, 0.0, 0.0] <------ Our dist_coeff
K: [1061.6538553425996, 0.0, 640.5, 0.0, 1061.6538553425996, 360.5, 0.0, 0.0, 1.0] <---- Our camera_matrix
R: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
P: [1061.6538553425996, 0.0, 640.5, -0.0, 0.0, 1061.6538553425996, 360.5, 0.0, 0.0, 0.0, 1.0, 0.0]
binning_x: 0
binning_y: 0
roi: 
  x_offset: 0
  y_offset: 0
  height: 0
  width: 0
  do_rectify: False
```
Thefore final value is
```
dist_coeff = [0.0, 0.0, 0.0, 0.0, 0.0]
camera_matrix = [[1061.6538553425996, 0.0, 640.5],[0.0, 1061.6538553425996, 360.5],[0.0, 0.0, 1.0]]
```
