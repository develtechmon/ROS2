# ROS2 Humble + Ubuntu 22.04.5 LTS + PX4 v1.13.3 + AirSim_Setup_Guide (Linux)
### Ubuntu 22.04 (Jammy Jellyfish)

> A comprehensive step-by-step guide based on real installation experience.
> Covers all known Ubuntu 22.04 compatibility issues and their fixes.

## Table of Contents
 
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Part 1 — Cosys-AirSim Installation](#part-1--cosys-airsim-installation)
4. [Part 2 — PX4 Installation](#part-2--px4-installation)
5. [Part 3 — Running PX4 + Gazebo](#part-3--running-px4--gazebo)
6. [Part 4 — Running PX4 + AirSim](#part-4--running-px4--airsim)
7. [Part 5 — Python API](#part-5--python-api)
8. [Quick Reference — All Fixes](#quick-reference--all-fixes)

## Overview
 
### Why Cosys-AirSim instead of Microsoft AirSim?
 
The original Microsoft AirSim has not been actively maintained since 2022 and was
built for Ubuntu 18.04. On Ubuntu 22.04 you will encounter these breaking issues:
 
| Error | Cause |
|-------|-------|
| `vulkan-utils` not found | Renamed to `vulkan-tools` in Ubuntu 22.04 |
| `clang-8` not found | Too old, not available in Ubuntu 22.04 repos |
| `libc++-8-dev` not found | Too old, not available in Ubuntu 22.04 repos |
| `cannot find -lstdc++` | Missing `libstdc++-12-dev` |
 
**Cosys-AirSim** is the actively maintained community fork that resolves all of
these out of the box for Ubuntu 22.04.
 
### Why PX4 v1.13?
 
PX4 v1.13 is the recommended version for use with AirSim/Cosys-AirSim. It is
well tested, stable, and compatible with Pixhawk v2.4.8 hardware when moving
from SITL to real hardware. Note that v1.13 setup scripts were written for
Ubuntu 20.04 and require several patches on Ubuntu 22.04 (all documented below).
 
### State Estimator — EKF2 vs LPE
 
PX4 v1.13 uses **EKF2** as the default and recommended state estimator. LPE is
deprecated and no longer maintained. All settings in this guide use EKF2.
 
---
 
## Prerequisites
 
- Ubuntu 22.04 LTS (Jammy Jellyfish)
- At least 25 GB free disk space
- Internet connection
- Git, curl installed
---

## Part 1 — Cosys-AirSim Installation

 
### Step 1.1 — Install System Dependencies
 
```bash
sudo apt-get update
sudo apt-get install -y \
    git \
    build-essential \
    cmake \
    python3-pip \
    libvulkan1 \
    vulkan-tools \
    clang-12 \
    clang++-12 \
    libc++-12-dev \
    libc++abi-12-dev \
    libstdc++-12-dev

sudo apt-get install clang-12
snap install cmake --classic
sudo apt install libc++-12-dev libc++abi-12-dev
sudo apt-get install -y clang-12 clang++-12 libc++-12-dev libc++abi-12-dev
pip3 install msgpack-rpc-python airsim
sudo apt-get install -y git python3-pip ninja-build python3-empy python3-toml python3-numpy python3-dev python3-setuptools
sudo apt install -y build-essential cmake git gcc g++ clang
sudo apt install -y libboost-all-dev libeigen3-dev libssl-dev uuid-dev
pip3 install kconfiglib jsonschema future
pip install --upgrade pip setuptools setuptools_scm wheel build
pip install msgpack==0.6.2 msgpack-python==0.5.6 msgpack-rpc-python==0.4.1
pip install --upgrade numpy
pip install pymavlink mavproxy
pip install airsim --no-build-isolation
```
Install `px4 dependencies`
```
# Install dependencies
sudo apt install -y \
    python3-pip \
    python3-jinja2 \
    python3-empy \
    python3-toml \
    python3-numpy \
    python3-yaml \
    python3-dev \
    ninja-build \
    exiftool \
    astyle

# Install additional tools
sudo apt install -y \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly
```

> **Note:** On Ubuntu 22.04, `vulkan-utils` was renamed to `vulkan-tools` and
> `clang-8` is no longer available. The packages above are the correct replacements.
 
### Step 1.2 — Clone Cosys-AirSim
 
```bash
cd ~
git clone https://github.com/Cosys-Lab/Cosys-AirSim.git
cd Cosys-AirSim
```
 
### Step 1.3 — Run Setup Script
 
```bash
./setup.sh
```
 
This downloads and configures AirLib dependencies. It completes without errors
on Ubuntu 22.04 since Cosys-AirSim already includes all compatibility fixes.
 
### Step 1.4 — Build AirSim
 
```bash
./build.sh
```
 
> This takes approximately 5-10 minutes depending on your machine.
 
After a successful build, binaries are located at below which we will use Actual Hardware Later using RPI:
 
```
~/Cosys-AirSim/build_release/output/bin/
├── MavLinkTest
├── DroneServer
└── ...
```
 
### Step 1.5 — Install Python Client
 
```bash
pip install airsim --no-build-isolation
```
 
> **Note on Python client naming:** The package `cosysairsim` is the Cosys-AirSim
> specific client. However, both `pip install airsim` and `pip install cosysairsim`
> use the same `import airsim` in your scripts — your existing code does not need
> to change. Use `cosysairsim` only if you need Cosys-AirSim specific APIs.
 
---

## Part 2 — PX4 Installation
 
### Step 2.1 — Clone PX4 v1.13.3
 
```bash
cd ~
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
git checkout v1.13.3
git submodule update --init --recursive
```
 
### Step 2.2 — Patch Setup Scripts for Ubuntu 22.04
 
Before running the setup script, apply these fixes to resolve Ubuntu 22.04
incompatibilities:
 
**Fix 1 — matplotlib version in requirements.txt:**
```bash
sed -i 's/matplotlib>=3.0\.\*/matplotlib>=3.0/g' Tools/setup/requirements.txt
```
 
**Fix 2 — Java version in ubuntu.sh:**

First it is important this java 17 version into our machine by running this command
```
sudo apt-get install -y openjdk-17-jdk openjdk-17-jre

test by 
java -version
```

And once the installation complete, Open the file and change `java_version=14` to `java_version=17`:
```bash
vi Tools/setup/ubuntu.sh
```
Find the line:
```
java_version=14
```
Change it to:
```
java_version=17
```
 
**Fix 3 — Remove gazebo package lines from apt install block:**
 
Open `Tools/setup/ubuntu.sh` and go to the `apt-get install` simulation
dependencies block (around line 227). Find and **delete** (do not comment out)
these two lines:
```
gazebo$gazebo_version \
...
libgazebo$gazebo_version-dev \
```
 
> **Important:** Do NOT use `#` to comment these lines out inside an `apt-get`
> multiline block — bash will treat `#gazebo11` as a command and fail. Delete
> the lines entirely.
 
### Step 2.3 — Run PX4 Ubuntu Setup Script
 
```bash
bash ./Tools/setup/ubuntu.sh --no-nuttx # (To skip building the firmware since we're using only for Simulation or SITL)
```
### Step 2.5 — Build PX4 SITL
 
After reboot, choose the build target based on your simulator:
 
**For AirSim (no Gazebo):**
```bash
cd ~/PX4-Autopilot
make px4_sitl_default none_iris
```
 
**For Gazebo Classic:**
```bash
cd ~/PX4-Autopilot
make px4_sitl_default gazebo_iris
```
 
> **Note on Gazebo target naming:** In PX4 v1.13, the Gazebo target is called
> `gazebo`, NOT `gazebo-classic`. The `gazebo-classic` name was introduced in
> PX4 v1.14+ to distinguish it from the new Gazebo (Harmonic/Garden).
 
The first build takes approximately 5-10 minutes.
 
---
 
## Part 3 — Running PX4 + Gazebo
 
### Step 3.1 — Launch PX4 + Gazebo
 
```bash
cd ~/PX4-Autopilot
make px4_sitl_default gazebo_iris
```
 
Gazebo window will open with an iris quadrotor on the ground and the PX4
interactive console will appear in the terminal.
 
### Step 3.2 — Disable Failsafe for SITL
 
By default PX4 triggers failsafe (RTL) when there is no RC or datalink.
In SITL this must be disabled. Run these in the PX4 console:
 
```bash
param set NAV_RCL_ACT 0
param set NAV_DLL_ACT 0
param set COM_RCL_EXCEPT 4
param set COM_OBL_ACT 1
```
 
> **⚠️ WARNING:** Never set these parameters on a real drone. They disable
> critical safety failsafes and are for SITL testing only.
 
### Step 3.3 — Test Takeoff
 
```bash
commander arm
commander takeoff
```
 
Expected output:
```
INFO  [commander] Armed by internal command
INFO  [navigator] Using minimum takeoff altitude: 2.50 m
INFO  [commander] Takeoff detected
```
 
The drone should rise to 2.5m in the Gazebo window.
 
### Step 3.4 — Headless Mode (Optional)
 
Run Gazebo without the GUI for faster simulation:
 
```bash
HEADLESS=1 make px4_sitl_default gazebo_iris
```
 
### Step 3.5 — Restarting a Session
 
Every time you stop the simulation, restart PX4 before starting a new session:
 
```bash
# Stop with Ctrl+C, then restart
make px4_sitl_default gazebo_iris
```
 
---
 
## Part 4 — Running PX4 + AirSim
 
### Step 4.1 — Configure AirSim settings.json
 
```bash
mkdir -p ~/Documents/AirSim
nano ~/Documents/AirSim/settings.json
```
 
Paste the following:
 
```json
{
    "SettingsVersion": 1.2,
    "SimMode": "Multirotor",
    "ClockType": "SteppableClock",
    "Vehicles": {
        "PX4": {
            "VehicleType": "PX4Multirotor",
            "UseSerial": false,
            "LockStep": true,
            "UseTcp": true,
            "TcpPort": 4560,
            "LocalHostIp": "127.0.0.1",
            "Sensors":{
                "Barometer":{
                    "SensorType": 1,
                    "Enabled": true,
                    "PressureFactorSigma": 0.0001825
                }
            },
            "Parameters": {
                "NAV_RCL_ACT": 0,
            		"NAV_DLL_ACT": 0,
            		"COM_OBL_ACT": 1,
            		"EKF2_AID_MASK": 1,
            		"EKF2_HGT_MODE": 0
            }
        }
    }
}
```
 
> **Note:** This uses EKF2 parameters (`EKF2_AID_MASK`, `EKF2_HGT_MODE`), NOT
> the old LPE parameters (`LPE_LAT`, `LPE_LON`) found in older AirSim docs.
> LPE is deprecated in PX4 v1.13.
 
### Step 4.2 — Launch PX4 SITL (Terminal 1)
 
```bash
cd ~/PX4-Autopilot
make px4_sitl_default none_iris
```
 
Wait until you see:
```
INFO [simulator] Waiting for simulator to connect on TCP port 4560
```
 
### Step 4.3 — Launch AirSim Blocks Environment (Terminal 2)
 
```bash
cd LinuxBlocks1.8.1/LinuxNoEditor
/Blocks.sh -ResX=1280 -ResY=720 -windowed
```
 
### Step 4.4 — Verify Connection
 
In the PX4 console you should see:
```
INFO [simulator] Simulator connected on UDP port 14560
INFO [mavlink] partner IP: 127.0.0.1
INFO [ecl/EKF] EKF GPS checks passed (WGS-84 origin set)
INFO [ecl/EKF] EKF commencing GPS fusion
```
 
### Step 4.5 — Disable Failsafe and Test
 
In the PX4 console:
```bash
param set NAV_RCL_ACT 0
param set NAV_DLL_ACT 0
param set COM_RCL_EXCEPT 4

commander arm
commander takeoff
```
 
### Switching Between Simulators
 
| Simulator | settings.json `UseSerial` | PX4 build target |
|-----------|--------------------------|-----------------|
| AirSim | `false` | `none_iris` |
| Gazebo | not needed | `gazebo_iris` |
| Real Pixhawk (HITL) | `true` | `none_iris` |
 
For real Pixhawk v2.4.8 (HITL), also add to settings.json:
```json
"SerialPort": "/dev/ttyUSB0,115200"
```
 
---
 
## Part 5 — Python API
 
### Basic connection test
 
```python
import airsim
 
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
 
# Takeoff
client.takeoffAsync().join()
 
# Hover for 5 seconds
import time
time.sleep(5)
 
# Land
client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)
```
 
### Get drone state
 
```python
import airsim
 
client = airsim.MultirotorClient()
client.confirmConnection()
 
state = client.getMultirotorState()
print("Position:", state.kinematics_estimated.position)
print("Velocity:", state.kinematics_estimated.linear_velocity)
```
 
---
 
## Quick Reference — All Fixes
 
### Cosys-AirSim Fixes
 
| Error | Fix |
|-------|-----|
| `E: Unable to locate package vulkan-utils` | Install `vulkan-tools` instead |
| `E: Package 'clang-8' has no installation candidate` | Install `clang-12` and `clang++-12` |
| `E: Unable to locate package libc++-8-dev` | Install `libc++-12-dev` and `libc++abi-12-dev` |
| `/usr/bin/ld: cannot find -lstdc++` | `sudo apt install libstdc++-12-dev` |
| CXX compiler broken in cmake | Install `libstdc++-12-dev`, delete `build_release/`, re-run `./build.sh` |
 
### PX4 Setup Fixes
 
| Error | Fix |
|-------|-----|
| `matplotlib>=3.0.*` pip error | Change to `matplotlib>=3.0` in `requirements.txt` |
| `E: Unable to locate package openjdk-14` | Change `java_version=14` to `java_version=17` in `ubuntu.sh` |
| `E: Unable to locate package gazebo11` | Delete `gazebo$gazebo_version \` line from apt block in `ubuntu.sh` |
| `gstreamer1.0-plugins-bad: command not found` | Caused by `#comment` inside apt multiline block — delete the line, don't comment it |
| `ninja: error: unknown target 'gazebo-classic'` | Use `gazebo_iris` not `gazebo-classic` for PX4 v1.13 |
 
### PX4 SITL Runtime Fixes
 
| Issue | Fix |
|-------|-----|
| Failsafe triggered, drone RTLs immediately | `param set NAV_RCL_ACT 0` and `param set NAV_DLL_ACT 0` |
| Takeoff denied | Wait for `home_set` message before arming |
| Drone lands after offboard command ends | `param set COM_OBL_ACT 1` (hover instead of land) |
| AirSim not connecting | Check TCP port 4560 is open, restart PX4 before AirSim |
 
---
 
## Complete Command Summary
 
### One-time setup
 
```bash
# === COSYS-AIRSIM ===
sudo apt-get update && sudo apt-get install -y \
    git build-essential cmake python3-pip \
    libvulkan1 vulkan-tools \
    clang-12 clang++-12 \
    libc++-12-dev libc++abi-12-dev libstdc++-12-dev
 
cd ~
git clone https://github.com/Cosys-Lab/Cosys-AirSim.git
cd Cosys-AirSim && ./setup.sh && ./build.sh
pip3 install airsim
 
# === PX4 ===
cd ~
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
git checkout v1.13.3
git submodule update --init --recursive
 
# Patch for Ubuntu 22.04
sed -i 's/matplotlib>=3.0\.\*/matplotlib>=3.0/g' Tools/setup/requirements.txt
# Manually edit Tools/setup/ubuntu.sh: java_version=14 -> java_version=17
# Manually remove gazebo$gazebo_version lines from apt block in ubuntu.sh
 
bash ./Tools/setup/ubuntu.sh
sudo reboot
```
 
### Every session — PX4 + Gazebo
 
```bash
cd ~/PX4-Autopilot
make px4_sitl_default gazebo_iris
 
# In PX4 console:
param set NAV_RCL_ACT 0
param set NAV_DLL_ACT 0
commander arm
commander takeoff
```
 
### Every session — PX4 + AirSim
 
```bash
# Terminal 1
cd ~/PX4-Autopilot
make px4_sitl_default none_iris
 
# Terminal 2 (after PX4 shows "Waiting for simulator")
cd ~/Cosys-AirSim
./Blocks.sh
```
 
---
 
*Guide based on real installation and troubleshooting experience on Ubuntu 22.04 Jammy.*
*Cosys-AirSim: https://github.com/Cosys-Lab/Cosys-AirSim*
*PX4 Autopilot: https://github.com/PX4/PX4-Autopilot*
 

 
