# PX4 FMUv2 Custom Firmware | HITL + Gazebo Classic | Flip Mode
## ROS1 | WSL2 | Ubuntu 20.04 | PX4 v1.14.3 Custom Build

> **Purpose:** Complete reproducible guide to build custom PX4 v1.14.3 firmware for FMUv2 (Pixhawk 1) with HITL support, connect to Gazebo Classic 11, and run autonomous flip + recovery via MAVROS.
>
> **Why custom firmware?** Stock PX4 v1.14.3 FMUv2 build excludes `pwm_out_sim` (motor sim output module) and blocks the HIL Quadcopter X airframe for FMUv2. Without these, HITL never works — Gazebo drone never moves regardless of parameters.
>
> **Hardware:** Pixhawk FMUv2, STM32F42x rev.5, 1MB flash limit

---

## Table of Contents

1. [Root Cause Analysis](#1-root-cause-analysis)
2. [Prerequisites](#2-prerequisites)
3. [Build Custom PX4 Firmware](#3-build-custom-px4-firmware)
4. [Flash Firmware via QGC](#4-flash-firmware-via-qgc)
5. [QGC Configuration](#5-qgc-configuration)
6. [PX4 Parameters](#6-px4-parameters)
7. [USB Forwarding to WSL2](#7-usb-forwarding-to-wsl2)
8. [Startup Sequence](#8-startup-sequence)
9. [Flip Script](#9-flip-script)
10. [Verification Checklist](#10-verification-checklist)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Root Cause Analysis

### Why Stock Firmware Fails for HITL

There are **three bugs** in stock PX4 v1.14.3 FMUv2 build that prevent HITL:

| Bug | Location | Effect |
|-----|----------|--------|
| `pwm_out_sim` not included | `boards/px4/fmu-v2/default.px4board` | Motor commands never reach Gazebo — drone never moves |
| HIL airframe excludes FMUv2 | `ROMFS/.../1001_rc_quad_x.hil` | HIL Quadcopter X never appears in QGC airframe list |
| `SYS_AUTOSTART` resets to 0 | Airframe exclusion causes failed init | `pwm_out_sim` exists but never starts |

**Fix:** Modify two files before building, then build custom firmware.

---

## 2. Prerequisites

### WSL2 Ubuntu 20.04

```bash
# Verify OS
lsb_release -a
# Expected: Ubuntu 20.04 LTS

# Verify ROS Noetic
roscore --version
# Expected: ROS Noetic

# Verify Gazebo 11
gazebo --version
# Expected: Gazebo multi-robot simulator, version 11.x.x

# Verify MAVROS
rospack find mavros
# Expected: path to mavros package
```

### PX4 Build Dependencies

```bash
cd ~/PX4-Autopilot

# Install PX4 build dependencies
bash ./Tools/setup/ubuntu.sh --no-nuttx

# Fix Python empy version (CRITICAL — wrong version breaks uORB generation)
pip3 install empy==3.3.4 --break-system-packages

# Install kconfiglib for boardconfig menu
pip3 install kconfiglib --break-system-packages

# Verify ARM toolchain
arm-none-eabi-gcc --version
# Expected: arm-none-eabi-gcc 10.x.x
```

### Verify PX4 Version

```bash
cd ~/PX4-Autopilot
git describe --tags
# Expected: v1.14.3
```

If not on v1.14.3:

```bash
git checkout v1.14.3
git submodule update --init --recursive
```

---

## 3. Build Custom PX4 Firmware

### 3.1 Fix 1: Enable HIL Airframe for FMUv2

The stock HIL Quadcopter X airframe explicitly excludes FMUv2. Without this fix, the airframe never appears in QGC.

```bash
# Check current state (shows exclude)
grep "board" ~/PX4-Autopilot/ROMFS/px4fmu_common/init.d/airframes/1001_rc_quad_x.hil

# Fix: change exclude to enable
sed -i 's/# @board px4_fmu-v2 exclude/# @board px4_fmu-v2 enable/' \
  ~/PX4-Autopilot/ROMFS/px4fmu_common/init.d/airframes/1001_rc_quad_x.hil

# Verify fix applied
grep "board" ~/PX4-Autopilot/ROMFS/px4fmu_common/init.d/airframes/1001_rc_quad_x.hil
# Expected: # @board px4_fmu-v2 enable
```

### 3.2 Fix 2: Add pwm_out_sim via boardconfig

`pwm_out_sim` is the module that sends motor commands from PX4 to Gazebo. Without it, the Gazebo drone never moves.

**Use the official PX4 boardconfig tool** — do NOT manually edit the px4board file:

```bash
cd ~/PX4-Autopilot
make px4_fmu-v2_default boardconfig
```

This opens an interactive terminal menu:

```
PX4 Firmware Configuration
*** Vendor: px4 ***
*** Model: fmu-v2 ***
*** Label: default ***
  Toolchain --->
[ ] Testing
[ ] Ethernet
  ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
```

**Navigation:**
- Arrow keys to move
- Enter to go into submenu
- Space to toggle enable/disable
- ESC to go back
- Q then Y to save and quit

**Path to pwm_out_sim:**

```
(scroll down) → Modules →
  (scroll down) → Simulation →
    [ ] pwm_out_sim    ← press SPACE to enable → [*] pwm_out_sim
```

Press **Q** → **Y** to save.

**Verify it was saved:**

```bash
grep "PWM_OUT_SIM" ~/PX4-Autopilot/boards/px4/fmu-v2/default.px4board
# Expected: CONFIG_MODULES_SIMULATION_PWM_OUT_SIM=y
```

### 3.3 Build Firmware

```bash
cd ~/PX4-Autopilot
make clean
make px4_fmu-v2_default 2>&1 | tail -10
```

**Expected output:**

```
Memory region    Used Size   Region Size   %age Used
         flash:   996461 B      1008 KB     96.54%    ← must be < 100%
          sram:    22932 B       192 KB     11.66%
[717/717] Creating px4_fmu-v2_default.px4
```

> ⚠️ If `region 'flash' overflowed` — firmware too large for 1MB. You must remove other modules via boardconfig to make room.

### 3.4 Copy Firmware to Windows

```bash
# Check your Windows username
ls /mnt/c/Users/

# Copy to Windows Downloads
cp ~/PX4-Autopilot/build/px4_fmu-v2_default/px4_fmu-v2_default.px4 \
   /mnt/c/Users/lukas/Downloads/px4_fmu-v2_default.px4
```

Or access directly via Windows Explorer:
```
\\wsl$\Ubuntu-20.04\home\jlukas\PX4-Autopilot\build\px4_fmu-v2_default\px4_fmu-v2_default.px4
```

---

## 4. Flash Firmware via QGC

1. Open **QGroundControl** on Windows
2. Connect Pixhawk via USB
3. Go to **Vehicle Setup** (gear icon) → **Firmware**
4. Disconnect then reconnect Pixhawk USB when prompted
5. Check **Advanced Settings**
6. Select **Custom firmware file...**
7. Browse to `C:\Users\lukas\Downloads\px4_fmu-v2_default.px4`
8. Click **OK**
9. Wait for flash to complete (~60 seconds)
10. Pixhawk reboots automatically

**Verify flash succeeded in QGC Summary:**
```
Firmware: PX4 Pro v1.14.3
```

---

## 5. QGC Configuration

### 5.1 Select HIL Airframe

After flashing:

1. QGC → **Vehicle Setup** → **Airframe**
2. Scroll down to **Simulation (Copter)** section
3. Select **HIL Quadcopter X** (yellow highlighted)
4. Click **Apply and Restart** (top right)
5. Wait for Pixhawk to reboot

> ⚠️ If HIL Quadcopter X does not appear — Fix 1 (airframe exclude→enable) was not applied before building. Rebuild with the fix.

### 5.2 Verify in NSH Console

QGC → **Analyze Tools** → **MAVLink Console**:

```bash
# Verify firmware version
ver all
# Expected: PX4 version: 1.14.3

# Verify pwm_out_sim is running with motor channels assigned
pwm_out_sim status
# Expected: Channel 0-3: func: 101, 102, 103, 104

# Verify HIL airframe loaded
param show SYS_AUTOSTART
# Expected: 1001

# Verify HITL mode active
param show SYS_HITL
# Expected: 1
```

---

## 6. PX4 Parameters

### 6.1 Set All Required Parameters

In QGC MAVLink Console (or NSH console):

```bash
# ── FAILSAFE DISABLE ──────────────────────────────────────────────────────────
param set NAV_RCL_ACT 0          # No RC loss failsafe (no RC in HITL)
param set NAV_DLL_ACT 0          # No data link loss failsafe
param set COM_RC_IN_MODE 4       # No RC controller required
param set COM_OBL_RC_ACT 1       # Hover when offboard ends (v1.14 name)

# ── FLIP PARAMETERS ───────────────────────────────────────────────────────────
param set FD_FAIL_R 0            # Disable roll failure detector
param set FD_FAIL_P 0            # Disable pitch failure detector
param set MC_ROLLRATE_MAX 1800   # Allow 30 rad/s flip roll rate
param set COM_OF_LOSS_T 5        # Offboard timeout 5 seconds
param set CBRK_FLIGHTTERM 121212 # Disable flight termination system

# ── FASTER VERTICAL RECOVERY ──────────────────────────────────────────────────
param set MPC_Z_VEL_P_ACC 8.0   # 2x faster altitude recovery after flip
param set MPC_Z_VEL_MAX_UP 6.0  # Faster upward climb after flip
param set MPC_ACC_UP_MAX 10.0   # Higher upward acceleration

# ── EKF2 GPS RELAXATION ───────────────────────────────────────────────────────
param set EKF2_GPS_CHECK 0       # Disable GPS quality checks
param set EKF2_REQ_EPH 5.0      # Relaxed horizontal accuracy
param set EKF2_REQ_EPV 8.0      # Relaxed vertical accuracy
param set EKF2_REQ_SACC 5.0     # Relaxed speed accuracy
param set EKF2_REQ_NSATS 4      # Minimum 4 satellites
param set EKF2_REQ_HDRIFT 0.3   # Relaxed horizontal drift
param set EKF2_REQ_VDRIFT 0.5   # Relaxed vertical drift

# ── ARMING ────────────────────────────────────────────────────────────────────
param set COM_ARM_WO_GPS 1       # Allow arming without GPS

# ── MAVLINK ───────────────────────────────────────────────────────────────────
param set MAV_1_CONFIG 0         # Disable TELEM2 MAVLink (prevents Tx overflow)

# ── SAVE AND REBOOT ───────────────────────────────────────────────────────────
param save
reboot
```

### 6.2 Parameter Reference Table

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `SYS_HITL` | `1` | Set automatically by HIL airframe — bypass real sensors |
| `NAV_RCL_ACT` | `0` | Disabled — no RC in HITL |
| `NAV_DLL_ACT` | `0` | Disabled — no data link failsafe |
| `COM_RC_IN_MODE` | `4` | No RC required |
| `COM_OBL_RC_ACT` | `1` | Hover when offboard ends |
| `FD_FAIL_R` | `0` | Allow full 360° roll for flip |
| `FD_FAIL_P` | `0` | Allow full 360° pitch |
| `MC_ROLLRATE_MAX` | `1800` | Allow 30 rad/s flip roll rate |
| `COM_OF_LOSS_T` | `5` | 5s offboard timeout |
| `CBRK_FLIGHTTERM` | `121212` | Disable flight termination |
| `MPC_Z_VEL_P_ACC` | `8.0` | Fast altitude recovery |
| `MPC_Z_VEL_MAX_UP` | `6.0` | Fast upward climb |
| `MPC_ACC_UP_MAX` | `10.0` | High upward acceleration |
| `EKF2_GPS_CHECK` | `0` | Accept Gazebo GPS immediately |
| `COM_ARM_WO_GPS` | `1` | Arm without GPS lock |
| `MAV_1_CONFIG` | `0` | Disable TELEM2 to prevent Tx overflow |

---

## 7. USB Forwarding to WSL2

Pixhawk connects via USB to Windows. WSL2 cannot see USB devices natively — use `usbipd-win` to forward.

### 7.1 Install usbipd-win (Windows — one time)

Open **PowerShell as Administrator**:

```powershell
winget install --interactive --exact dorssel.usbipd-win
```

Restart Windows after installation.

### 7.2 Attach Pixhawk to WSL2 (every session)

Plug in Pixhawk USB. In **PowerShell as Administrator**:

```powershell
# List USB devices — find Pixhawk BUSID
usbipd list
# Look for: PX4 FMU or similar, note BUSID (e.g. 1-1)

# Bind once (survives reboots)
usbipd bind --busid 1-1

# Attach to WSL2
usbipd attach --wsl --busid 2-1
```

### 7.3 Verify in WSL2

```bash
ls /dev/ttyACM0
# Expected: /dev/ttyACM0

sudo chmod 666 /dev/ttyACM0

# Verify baud rate PX4 is using
stty -F /dev/ttyACM0 speed
# Note this value — must match iris_hitl.sdf baudRate
```

---

## 8. Startup Sequence

> ⚠️ **Critical order.** Follow exactly. Wrong order = connection failures.

### Step 1: Configure iris_hitl.sdf

Set baud rate to match what PX4 actually runs (`mavlink status` shows the value):

```bash
vi ~/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_hitl/iris_hitl.sdf
```

Key settings:

```xml
<serialEnabled>1</serialEnabled>
<serialDevice>/dev/ttyACM0</serialDevice>
<baudRate>2000000</baudRate>      <!-- match PX4 mavlink status output -->
<hil_mode>1</hil_mode>
<enable_lockstep>0</enable_lockstep>   <!-- must be 0 for HITL -->
```

### Step 2: Build Gazebo Plugins (one time)

```bash
cd ~/PX4-Autopilot
DONT_RUN=1 make px4_sitl_default gazebo-classic
```

### Step 3: Close QGC on Windows Completely

Right-click QGC in taskbar → Quit. QGC must not be running when Gazebo starts.

### Step 4: Attach Pixhawk to WSL2

```powershell
# PowerShell as Admin (Windows)
usbipd attach --wsl --busid 1-1
```

```bash
# WSL2 — verify
ls /dev/ttyACM0
sudo chmod 666 /dev/ttyACM0
```

### Step 5: Start Gazebo (Terminal 1)

```bash
cd ~/PX4-Autopilot

source Tools/simulation/gazebo-classic/setup_gazebo.bash \
  $(pwd) $(pwd)/build/px4_sitl_default

export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/simulation/gazebo-classic/sitl_gazebo-classic

gazebo Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds/hitl_iris.world --verbose
```

Wait for these messages:

```
[Msg] Connecting to PX4 SITL using serial
[Msg] Opened serial device /dev/ttyACM0
```

> ⚠️ If you see `Tx queue overflow` — baud rate mismatch. Check `mavlink status` in NSH console and update `<baudRate>` in iris_hitl.sdf to match.

### Step 6: Verify EKF2 Initialized

Wait 10–15 seconds after Gazebo connects, then check in NSH console:

```bash
ekf2 status
```

Expected:

```
attitude: 1, local position: 1, global position: 1
```

If still `0, 0, 0` — Gazebo not sending sensor data. Check baud rate and serial connection.

Force home position if needed:

```bash
commander set_home 1
```

### Step 7: Start MAVROS (Terminal 2)

```bash
source /opt/ros/noetic/setup.bash

roslaunch mavros px4.launch \
  fcu_url:="udp://:14550@127.0.0.1:14555" \
  tgt_system:=1 \
  tgt_component:=1
```

Wait for:

```
[ INFO] CON: Got HEARTBEAT, connected. FCU: PX4 Autopilot
[ INFO] VER: 1.1: Flight software: ...1.14.3...
```

### Step 8: Verify MAVROS State (Terminal 3)

```bash
rostopic echo /mavros/state -n 1
```

Expected:

```
connected: True
armed: False
mode: ""
system_status: 3    ← STANDBY (not 8=TERMINATION)
```

### Step 9: Run Flip Script (Terminal 3)

```bash
source /opt/ros/noetic/setup.bash
python3 drone_sitl_flip_gazebo.py
```

---

## 9. Flip Script

Same Gazebo-tuned script as SITL. Save as `drone_sitl_flip_gazebo.py`:

```python
#!/usr/bin/env python3
import rospy
import math
import threading
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State, AttitudeTarget
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest

current_state = State()
current_pose  = PoseStamped()

def state_cb(msg):
    global current_state
    current_state = msg

def pose_cb(msg):
    global current_pose
    current_pose = msg

rospy.init_node('flip_node')
state_sub = rospy.Subscriber('mavros/state', State, state_cb)
pose_sub  = rospy.Subscriber('mavros/local_position/pose', PoseStamped, pose_cb)
pos_pub   = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
att_pub   = rospy.Publisher('mavros/setpoint_raw/attitude', AttitudeTarget, queue_size=10)

rospy.wait_for_service('/mavros/cmd/arming')
rospy.wait_for_service('/mavros/set_mode')
arming_client   = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)

setpoint_lock = threading.Lock()
current_setpoint = {
    'mode': 'pos', 'x': 0.0, 'y': 0.0, 'z': 3.0,
    'roll_rate': 0.0, 'pitch_rate': 0.0, 'yaw_rate': 0.0, 'thrust': 0.5
}

def update_pos(x, y, z):
    with setpoint_lock:
        current_setpoint.update({'mode': 'pos', 'x': x, 'y': y, 'z': z})

def update_rate(roll_rate, pitch_rate, yaw_rate, thrust):
    with setpoint_lock:
        current_setpoint.update({
            'mode': 'rate', 'roll_rate': roll_rate,
            'pitch_rate': pitch_rate, 'yaw_rate': yaw_rate, 'thrust': thrust
        })

def bg_publish():
    r = rospy.Rate(50)
    while not rospy.is_shutdown():
        with setpoint_lock:
            sp = dict(current_setpoint)
        if sp['mode'] == 'pos':
            msg = PoseStamped()
            msg.header.stamp = rospy.Time.now()
            msg.pose.position.x = sp['x']
            msg.pose.position.y = sp['y']
            msg.pose.position.z = sp['z']
            msg.pose.orientation.w = 1.0
            pos_pub.publish(msg)
        else:
            msg = AttitudeTarget()
            msg.header.stamp = rospy.Time.now()
            msg.type_mask    = 128   # IGNORE_ATTITUDE: use body rates + thrust
            msg.body_rate.x  = sp['roll_rate']
            msg.body_rate.y  = sp['pitch_rate']
            msg.body_rate.z  = sp['yaw_rate']
            msg.thrust       = sp['thrust']
            att_pub.publish(msg)
        r.sleep()

threading.Thread(target=bg_publish, daemon=True).start()

def get_roll():
    o = current_pose.pose.orientation
    return math.atan2(2*(o.w*o.x + o.y*o.z), 1 - 2*(o.x**2 + o.y**2))

def get_pos():
    p = current_pose.pose.position
    return p.x, p.y, p.z

def sleep_publishing(seconds):
    end = rospy.Time.now() + rospy.Duration(seconds)
    while rospy.Time.now() < end and not rospy.is_shutdown():
        rospy.sleep(0.01)

def wait_until_stable(target_z=20.0, roll_threshold=5.0, timeout=30.0):
    rospy.loginfo(f"Waiting for stability...")
    update_pos(0, 0, target_z)
    start = rospy.Time.now()
    while not rospy.is_shutdown():
        roll_deg = math.degrees(get_roll())
        x, y, z  = get_pos()
        rospy.loginfo(f"  Stability: roll={roll_deg:.1f}deg  z={z:.2f}")
        if abs(roll_deg) < roll_threshold and z > target_z - 2.0:
            rospy.loginfo("Stable!")
            return True
        if (rospy.Time.now() - start).to_sec() > timeout:
            rospy.logwarn("Timeout — proceeding.")
            return False
        rospy.sleep(0.3)

def flip(direction='right'):
    sx, sy, sz = get_pos()
    rospy.loginfo(f"[FLIP {direction.upper()}] z={sz:.2f}")
    # Phase 1: Thrust bump
    update_rate(0, 0, 0, 1.0)
    sleep_publishing(0.2)
    # Phase 2: Roll — thrust 0.55 > MPC_THR_HOVER=0.50
    roll_rate = 30.0 if direction == 'right' else -30.0
    update_rate(roll_rate, 0, 0, 0.55)
    timeout = rospy.Time.now() + rospy.Duration(3.0)
    while not rospy.is_shutdown() and rospy.Time.now() < timeout:
        roll = get_roll()
        rospy.loginfo(f"  roll={math.degrees(roll):.1f}deg")
        if abs(roll) > math.pi / 2:
            rospy.loginfo(f"  Flipped!")
            break
        rospy.sleep(0.01)
    # Phase 3: Counter-roll
    counter_rate = -50.0 if direction == 'right' else 50.0
    update_rate(counter_rate, 0, 0, 0.9)
    sleep_publishing(0.20)
    # Phase 4: Recover
    update_pos(sx, sy, sz)
    sleep_publishing(3.0)
    rospy.loginfo(f"[FLIP {direction.upper()}] Done! z={get_pos()[2]:.2f}")

# Main
rospy.loginfo("Waiting for FCU connection...")
while not rospy.is_shutdown() and not current_state.connected:
    rospy.sleep(0.1)
rospy.loginfo("Connected!")

rospy.loginfo("Pre-streaming setpoints for 5 seconds...")
update_pos(0, 0, 3)
sleep_publishing(5.0)

offb = SetModeRequest(); offb.custom_mode = 'OFFBOARD'
arm  = CommandBoolRequest(); arm.value = True
last_req    = rospy.Time.now()
rate        = rospy.Rate(20)
phase       = "TAKEOFF"
phase_start = rospy.Time.now()

while not rospy.is_shutdown():
    if current_state.mode != "OFFBOARD" and \
       (rospy.Time.now() - last_req) > rospy.Duration(5.0):
        if set_mode_client.call(offb).mode_sent:
            rospy.loginfo("OFFBOARD enabled!")
        last_req = rospy.Time.now()
    elif not current_state.armed and \
         (rospy.Time.now() - last_req) > rospy.Duration(5.0):
        if arming_client.call(arm).success:
            rospy.loginfo("Armed!")
        last_req = rospy.Time.now()

    x, y, z  = get_pos()
    roll_deg = math.degrees(get_roll())

    if phase == "TAKEOFF":
        update_pos(0, 0, 3)
        if current_state.armed and z > 2.5:
            rospy.loginfo(f"Takeoff complete. z={z:.2f}")
            phase = "CLIMB"
    elif phase == "CLIMB":
        update_pos(0, 0, 20)
        if z > 18.0:
            rospy.loginfo(f"Flip altitude reached. z={z:.2f}")
            phase = "STABILIZE_1"
            phase_start = rospy.Time.now()
    elif phase == "STABILIZE_1":
        update_pos(0, 0, 20)
        if (rospy.Time.now() - phase_start).to_sec() > 3.0:
            rospy.loginfo("Ready for first flip!")
            phase = "FLIP_RIGHT"
    elif phase == "FLIP_RIGHT":
        flip('right')
        phase = "STABILIZE_2"
    elif phase == "STABILIZE_2":
        wait_until_stable(target_z=20.0, roll_threshold=5.0, timeout=30.0)
        rospy.loginfo("Ready for second flip!")
        phase = "FLIP_LEFT"
    elif phase == "FLIP_LEFT":
        flip('left')
        phase = "DONE"
    elif phase == "DONE":
        update_pos(0, 0, 3)
        rospy.loginfo(f"All flips complete! z={z:.2f} roll={roll_deg:.1f}deg")
        sleep_publishing(5.0)
        break

    rate.sleep()

rospy.loginfo("Script complete.")
```

---

## 10. Verification Checklist

Run through this every session before launching the script:

```bash
# 1. Pixhawk visible in WSL2
ls /dev/ttyACM0                          # must exist

# 2. Correct firmware
# NSH: ver all                           # must show 1.14.3

# 3. pwm_out_sim running with motors assigned
# NSH: pwm_out_sim status                # Channel 0-3: func 101-104

# 4. HIL airframe loaded
# NSH: param show SYS_AUTOSTART          # must be 1001

# 5. HITL enabled
# NSH: param show SYS_HITL               # must be 1

# 6. Gazebo connected
# Gazebo terminal: "Opened serial device /dev/ttyACM0"

# 7. EKF2 initialized
# NSH: ekf2 status                       # attitude:1 local:1 global:1

# 8. MAVROS connected
rostopic echo /mavros/state -n 1         # connected:True system_status:3

# 9. No Tx overflow in Gazebo terminal
# Gazebo: no "Tx queue overflow" messages
```

---

## 11. Troubleshooting

| Problem | Fix |
|---------|-----|
| HIL Quadcopter X missing in QGC | Fix 1 not applied — rebuild with `# @board px4_fmu-v2 enable` |
| `pwm_out_sim: command not found` | Fix 2 not applied — rebuild with pwm_out_sim enabled in boardconfig |
| `pwm_out_sim: not running` | Wrong airframe — select HIL Quadcopter X in QGC and reboot |
| `SYS_AUTOSTART = 0` after reboot | HIL airframe excluded from FMUv2 — apply Fix 1 and rebuild |
| `Tx queue overflow` in Gazebo | Baud rate mismatch — check `mavlink status` in NSH, update `<baudRate>` in iris_hitl.sdf |
| `ekf2: attitude:0 local:0` | Gazebo not sending sensor data — baud rate mismatch or serial not connected |
| `system_status: 8` (TERMINATION) | EKF2 not initialized — fix baud rate, wait longer after Gazebo connects |
| `/dev/ttyACM0 not found` | usbipd not attached — run `usbipd attach --wsl --busid X` in PowerShell |
| `region 'flash' overflowed` | Firmware too large — remove unused modules via boardconfig |
| `empy has no attribute RAW_OPT` | Wrong empy version — `pip3 install empy==3.3.4 --break-system-packages` |
| Drone arms but doesn't move in Gazebo | `pwm_out_sim` not running — check airframe selection and reboot |

---

## Appendix: Quick Reference

### Build Commands

```bash
# Fix airframe (once per checkout)
sed -i 's/# @board px4_fmu-v2 exclude/# @board px4_fmu-v2 enable/' \
  ~/PX4-Autopilot/ROMFS/px4fmu_common/init.d/airframes/1001_rc_quad_x.hil

# Open boardconfig and enable pwm_out_sim under Modules → Simulation
make px4_fmu-v2_default boardconfig

# Build
make clean && make px4_fmu-v2_default

# Copy to Windows
cp build/px4_fmu-v2_default/px4_fmu-v2_default.px4 /mnt/c/Users/lukas/Downloads/
```

### Startup Commands (Every Session)

```bash
# Windows PowerShell (Admin)
usbipd attach --wsl --busid 2-1

# WSL2 Terminal 1 — Gazebo
cd ~/PX4-Autopilot
source Tools/simulation/gazebo-classic/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/simulation/gazebo-classic/sitl_gazebo-classic
gazebo Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds/hitl_iris.world --verbose

# WSL2 Terminal 2 — MAVROS (after Gazebo shows "Opened serial device")
source /opt/ros/noetic/setup.bash
roslaunch mavros px4.launch fcu_url:="udp://:14550@127.0.0.1:14555" tgt_system:=1 tgt_component:=1

# WSL2 Terminal 3 — Flip Script (after MAVROS connected)
source /opt/ros/noetic/setup.bash
python3 drone_sitl_flip_gazebo.py
```

### The Two Root Cause Fixes

```
Fix 1: 1001_rc_quad_x.hil
  BEFORE: # @board px4_fmu-v2 exclude   ← HIL frame hidden from QGC
  AFTER:  # @board px4_fmu-v2 enable    ← HIL frame visible in QGC

Fix 2: boards/px4/fmu-v2/default.px4board
  ADD: CONFIG_MODULES_SIMULATION_PWM_OUT_SIM=y  ← via boardconfig menu
  WITHOUT THIS: Gazebo drone never moves
```

---

*Generated: May 2026 | PX4 v1.14.3 Custom FMUv2 | ROS Noetic | Ubuntu 20.04 WSL2 | Gazebo Classic 11*
