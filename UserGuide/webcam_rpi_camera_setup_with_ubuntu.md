## Getting Started

This is user guide on how to enable `IMX219 Noir` camera and `USB webcam` camera in `Ubuntu`
For this guide i'm using `Logitech Webcam` and `IMX219 Noir ` camera. RPi Camera module 3 is not working from ym test.

## Step 1 : Install Following Packages

Install open `CV` first
```
pip install opencv-contrib-python
```

Then install following packages
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install ffmpeg libsm6 libxext6
```

## Step 2 : Install `Raspi Config` in `Ubuntu` - Please remember this is for Rpi Camera. For USB webcam, can skip directly to Step 3
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
camera_auto_detect=1
display_auto_detect=1
start_x=1 <--- This one
```

## Step 4 : Verify that you should able to see `dev/video` as follow.
```
ls /dev/video0 <---- This show we have video devices
```
## Step 5 : Verify latest `config.txt` file as follow:

```
[all]
kernel=vmlinuz
cmdline=cmdline.txt
initramfs initrd.img followkernel

[pi4]
dtoverlay=vc4-fkms-v3d
max_framebuffers=2
arm_boost=1

[all]
# Enable the audio output, I2C and SPI interfaces on the GPIO header. As these
# parameters related to the base device-tree they must appear *before* any
# other dtoverlay= specification
dtparam=audio=on
dtparam=i2c_arm=on
dtparam=spi=on

# Comment out the following line if the edges of the desktop appear outside
# the edges of your display
disable_overscan=1

# If you have issues with audio, you may try uncommenting the following line
# which forces the HDMI output into HDMI mode instead of DVI (which doesn't
# support audio output)
#hdmi_drive=2

# Enable the serial pins
enable_uart=1

# Autoload overlays for any recognized cameras or displays that are attached
# to the CSI/DSI ports. Please note this is for libcamera support, *not* for
# the legacy camera stack
start_x=1
display_auto_detect=1
start_x=1

# Config settings specific to arm64
arm_64bit=1
dtoverlay=dwc2

[cm4]
# Enable the USB2 outputs on the IO board (assuming your CM4 is plugged into
# such a board)
dtoverlay=dwc2,dr_mode=host

[all]
gpu_mem=128 <---- This one
```

If you camera doesn't work. It's most probably caused by the camera setup. In my case, i'm using `IMX219 NoIR` camera.
Therefore, please check your connection carefully.
