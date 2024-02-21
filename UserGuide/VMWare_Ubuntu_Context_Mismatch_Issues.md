# Getting Started

If you're using VMWare, you may encounter following message when you launching your `Gazebo`. 
In my case, i'm using VMWare Ubuntu 20.0. Ros2 foxy. To solve this problem, use following command

Error `context mismatch in svga surface destroy gazebo`

Solution

To set it for one session of Bash, use:
```
export SVGA_VGPU10=0
```

To permanently write it to the Bash user settings:
```
echo "export SVGA_VGPU10=0" >> ~/.bashrc
```
