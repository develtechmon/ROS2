# ROS2 Humble + Ubuntu 22.04.5 LTS + PX4 v1.13.3 + Pixhawk + AirSim_HITL_Setup_Guide (Linux)
### Ubuntu 22.04 (Jammy JellyFish)

> This is step by step guide on how to enable HITL simulation using Pixhawk Flight Controller.
> The step is quite broad but we'll do it step by step.

### Step 1: Please ensure you've follow this guide 1st before we proceed further.
```
/ROS2_Humble_Ubuntu_22_PX4_v1.13.3_AirSim_Setup_Guide.md
```

### Step 2: Download QGroundControl and Flash Firmware

Install dependencies first
```

sudo usermod -a -G dialout $USER
sudo apt-get remove modemmanager -y
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
sudo apt install libqt5gui5 -y
sudo apt install libfuse2 -y
```

`libfuse2` is the Ubuntu 22.04 specific requirement — QGC won't start on clean Ubuntu 22.04 without it because of a missing `libfuse.so.2.` PX4

```
cd ~/Downloads
wget https://github.com/mavlink/qgroundcontrol/releases/download/v4.4.0/QGroundControl.AppImage
chmod +x QGroundControl.AppImage
```

Or get the latest v4.4.x from the releases page directly:
```
https://github.com/mavlink/qgroundcontrol/releases
```

Run it
```
./QGroundControl.AppImage
```

For your `setup` we use QGC for 
```
QGroundControl ← monitors, configures, flashes firmware
Now (SITL) — monitor what PX4 is doing during PPO training, check EKF status, verify GPS lock, watch attitude estimates in real time.
HITL setup — flash the HIL Quadrocopter X airframe to your Pixhawk, set parameters like NAV_RCL_ACT=0, MAV_PROTO_VER=1.
Real drone — pre-flight parameter verification before you ever arm motors.
```

For my setup, i'm using `pixhawk v2.4.8`. For this version of FC, it supported only `px4_fmu-v2_default.px4`. In this setup, i'm using
version `1.9.2`. Below is the details of firmware i'm using and you can use `ver hw` command to check for hardware version and `ver git` to check
firmware version using `MAVLINK console` in QGC.
```
nsh> ver hw
HW arch: PX4_FMU_V2
HW type: V30
HW version: 0x0009000E
HW revision: 0x00000000
nsh> ver git
FW git-hash: 106905871d374c125730fe675266d67c7f869469
FW version: Release 1.9.2 (17367807)
OS: NuttX
OS version: Release 7.28.0 (119275775)
OS git-hash: 423371c7d4012e725ac4ca51323a18df64e581b3
nsh> 
```

You can download the `px4_fmu-v2_default.px4` version `v1.9.2` at this link
```
https://github.com/PX4/PX4-Autopilot/releases/tag/v1.9.2
```

Flash the firmware to PX4 using QGC by disconnection and connecting the `flight controller`. Please select advanced to upload and flash the downloaded above firmware
into our `Pixhawk`.

### Step 3: Check the following parameter in our `QGC`.

Please connect the pixhak again to computer, QGC should detect the Pixhawk port aautomatically.

Before we writng or change the parameter value, please run the following command in MAVLINK console
```
pwm_out_sim status
```

It if responds, the `HITL` path work which is OK. Output as follow
```
nsh> pwm_out_sim status
INFO  [pwm_out_sim] Running max update rate: 400 Hz
INFO  [pwm_out_sim] Polling 2 actuator controls
INFO  [pwm_out_sim] PWM Mode: pwm16
```

## Step 4: Configure HITL airframcne in QGC.

To run `hardware in loop` using Pixhawk and utilizing `Airsim physic` we need enable `HIL` as follow. This is very
important step.

In QGC, configure HITL airframe
```
Vehicle Setup → Airframe → scroll down to find HIL Quadcopter X → select it → Apply and Restart.
```

In QGC --> Safety settings.
```
Vehicle Setup → Safety → set HITL Enabled to Enabled.
```

Reboot the drone.

### Step 5 : Set the following parameter under `Vehicle Setup` --> `Parameters`.

Once the drone successfuly reboot you should refer to arrow below and set the parameter as follow under

```
Symbols: x = used, + = saved, * = unsaved
x + BAT_A_PER_V [1,1] : 15.3910
x + BAT_CNT_V_CURR [3,3] : 0.0008
x + BAT_CNT_V_VOLT [4,4] : 0.0008
x + BAT_V_DIV [12,12] : 10.1779
x + CAL_ACC0_ID [16,17] : 2162698
x + CAL_GYRO0_ID [20,46] : 2162698
x + CAL_MAG0_ID [21,71] : 396817
x + CAL_MAG0_ROT [22,72] : 0
x + CBRK_USB_CHK [38,116] : 197848
x + CBRK_VELPOSERR [39,117] : 201607
x + COM_ARM_WO_GPS [43,130] : 1 <-------
x + COM_FLIGHT_UUID [52,139] : 7
x + COM_OBL_ACT [65,152] : 1 <-------
x + COM_RC_IN_MODE [76,163] : 4 
x + EKF2_AID_MASK [93,180] : 1
x + EKF2_BARO_NOISE [101,188] : 0.5000 <-------
x + EKF2_GPS_CHECK [120,207] : 0 <-------
x + EKF2_HGT_MODE [135,222] : 0
x + EKF2_MAG_DECL [147,234] : 15.5283
x + EKF2_REQ_EPH [172,259] : 5.0000
x + EKF2_REQ_EPV [173,260] : 8.0000
x + EKF2_REQ_SACC [177,264] : 5.0000
x + GPS_1_CONFIG [210,388] : 0
x + LNDMC_FFALL_THR [214,406] : 0.1000
x + LNDMC_ROT_MAX [217,409] : 40.0000
x + LNDMC_XY_VEL_MAX [218,410] : 10.0000
x + LNDMC_Z_VEL_MAX [219,411] : 10.0000
x + LND_FLIGHT_T_HI [220,412] : 0
x + LND_FLIGHT_T_LO [221,413] : 1489747648
x + MAV_PROTO_VER [234,432] : 1
x + MPC_TKO_SPEED [320,533] : 1.5000
x + MPC_XY_VEL_MAX [329,542] : 2.0000
x + MPC_Z_VEL_MAX_UP [340,553] : 3.0000 <-------
x + NAV_DLL_ACT [346,559] : 0 <-------
x + NAV_RCL_ACT [367,580] : 0  <-------
x + SYS_AUTOSTART [596,871] : 1001
x + SYS_HITL [606,883] : 1 <-------
x + SYS_RESTART_TYPE [609,886] : 0 

 621/1080 parameters used.

```

You can set the param as follow in `Mavlink Console` for example.
```
param set SYS_HITL 1
param save
reboot
```

After reboot, verify in MAVLINK console
```
param show SYS_HITL
```

Also check `pwm_out_sim` is set to start automatically
```
param show SYS_AUTOSTART
```

For `HIL Quadcopter X` this should be 1001 as follow:
```
param show SYS_AUTOSTART
Symbols: x = used, + = saved, * = unsaved
x + SYS_AUTOSTART [597,871] : 1001

 622/1080 parameters used.
nsh> 
```
