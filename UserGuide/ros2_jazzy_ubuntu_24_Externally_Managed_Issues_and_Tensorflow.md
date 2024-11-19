# Getting Started


This is userguide on how to remove the `externally manage` issue when you want to install `pip` python package in `RPi5`.

My spec and components as follow
```
Ubuntu 24.04.1 LTS aarch64
ROS2 Jazzy
Raspberry Pi 5 4GB
```

To remove `externally manage` permission, please do the following

Make backup and move to Desktop
```
sudo mv /usr/lib/python3.12/EXTERNALLY-MANAGED ~develtechmon/Desktop/
```

Or Delete
```
sudo rm -rf /usr/lib/python3.12/EXTERNALLY-MANAGED
```

Then install `Tensorflow` package
```
sudo pip3 install tensorflow
```
