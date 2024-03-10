# Getting Started

To install barrier in ubuntu 22 follow this step
```
sudo apt-get -y install barrier

sudo apt-get install net-tools
```

Disable `ssl` and add the pc name accordingly.

In case if mouse is not working at other computer. Follow below method
```
sudo vi /etc/gdm3/custom.conf

Inside this file, uncomment following line
---> #WaylandEnable=false (before)
---> WaylandEnable=false  (after)

Restart the service in new terminal
sudo systemctl restart gdm3
```

You should see the mouse is working now.

Link
```
https://askubuntu.com/questions/1407275/mouse-disappears-while-using-barrier
```
