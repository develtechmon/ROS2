## Getting Started

This is user guide on how to enable `IMX219 Noir` camera and `USB webcam` camera in `Ubuntu`
For this guide i'm using `Logitech Webcam` and `IMX219 Noir ` camera. RPi Camera module 3 is not working from ym test.

## Step 1 : Install Following Packages
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install ffmpeg libsm6 libxext6 -y
```

## Step 2 : Install `Raspi Config` in `Ubuntu`
```
sudo apt install raspi-config
```
and then run 
```
sudo raspi-config
```
From the menu, enable `Legacy Camera Enable/disable legacy camera support` and then `Save` and `reboot` the `Rpi`

## Step 3 : Edit the `Config.txt` file.

Go to
```
sudo vi /boot/firmware/config.txt
```
and then add `start_x=1` into the `config.txt` file as follow
```
# Autoload overlays for any recognized cameras or displays that are attached
# to the CSI/DSI ports. Please note this is for libcamera support, *not* for
# the legacy camera stack
start_x=1
display_auto_detect=1
start_x=1 <---- This one
```

## Step 4 : Verify that you should able to see `dev/video` as follow.
```
ls /dev/video0 <---- This show we have video devices
```