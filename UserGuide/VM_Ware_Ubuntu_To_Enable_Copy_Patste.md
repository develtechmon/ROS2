# Getting Started

I've have problem to enable `COPY` and `PASTE` function between my windows to VM Machine ubuntu.
This is very tedious.

To enable `COPY` and `PASTE` options, at least this is working for mw. Other might suggest to enable option
is `GUEST ISOLATION` but i cant find them.

## 1. Go to `VM Machine Ubuntu`
open your terminal and copy and install following code
```
sudo apt-get install open-vm-tools
sudo apt-get install open-vm-tools-desktop
```

And the `reboot` your VM ubuntu machine
```
sudo reboot now
```
You should now able to copy and paste between 2 machines (Windows and Ubuntu)
