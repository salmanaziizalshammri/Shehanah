# 🛰️ SHEHANAH — Autonomous Drone Interception System

> A low-cost, AI-based autonomous UAV capable of detecting, tracking, and intercepting aerial threats in real time.

-----

## 📌 Overview

**SHEHANAH** is a fully autonomous interceptor drone system built to address the growing challenge of detecting and neutralizing low-radar-signature drones. It leverages Python, MAVSDK, and PX4 to deliver real-time autonomous decision-making — without human intervention.

Traditional air defense systems are expensive and often ineffective against small, stealthy UAVs. SHEHANAH offers a scalable, low-cost alternative designed for smart air security.

-----

## ✨ Features

- 🔍 **Radar-based detection** — Detects and tracks incoming aerial targets in real time
- ⚡ **Fully autonomous operation** — No manual input required from detection to interception
- 🧠 **State machine control** — Manages system states: `WAIT → LAUNCH → INTERCEPT → END`
- 🚁 **PX4 flight control** — Handles UAV dynamics, stability, and altitude synchronization
- 📡 **MAVSDK communication** — Manages all communication between system components and the drone
- 💡 **Dynamic interception logic** — Continuously adjusts speed and trajectory to close distance
- 💰 **Low-cost architecture** — A practical alternative to expensive air defense systems
- 📈 **Scalable design** — Can be extended for larger deployments

-----

## 🏗️ System Architecture

```
Radar Detection Module
    └── Detects and tracks aerial objects in real time

State Machine Controller
    └── Manages system states from detection to interception

Flight Control (PX4)
    └── Controls UAV flight dynamics and stability

MAVSDK Communication
    └── Handles communication between system components and the UAV

Interception Logic
    └── Determines interception strategy and execution timing
```

-----

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- [MAVSDK-Python](https://github.com/mavlink/MAVSDK-Python)
- [PX4 Autopilot](https://px4.io/) (or a compatible simulator like Gazebo)
- A SITL (Software In The Loop) simulator for testing

### Steps

1. **Clone the repository**
   
   ```bash
   git clone https://github.com/your-username/shehanah.git
   cd shehanah
   ```
1. **Install dependencies**
   
   ```bash
   pip install mavsdk asyncio
   ```
1. **Start PX4 SITL simulator** (for testing)
   
   ```bash
   make px4_sitl gazebo
   ```
1. **Run the SHEHANAH system**
   
   ```bash
   python shehanah.py
   ```

-----

## 🔧 Configuration

All key parameters are defined at the top of `shehanah.py`:

|Parameter     |Value  |Description                    |
|--------------|-------|-------------------------------|
|`RADAR_START` |140.0 m|Begin airspace monitoring      |
|`RADAR_REPORT`|120.0 m|Trigger threat status report   |
|`RADAR_LAUNCH`|110.0 m|Authorize SHEHANAH launch      |
|`TARGET_ALT`  |30.0 m |Assumed target flight altitude |
|`TARGET_SPEED`|1.0 m/s|Simulated target approach speed|
|`SHEHANAH_ALT`|50.0 m |SHEHANAH cruise altitude       |
|`FOLLOW_SPEED`|2.5 m/s|SHEHANAH interception speed    |

-----

## 🚀 Usage

Once running, SHEHANAH operates through the following autonomous flow:

### 1. Detection Phase

The radar module monitors airspace. Alerts trigger at two thresholds before launch:

|Threshold     |Distance|Action                     |
|--------------|--------|---------------------------|
|`RADAR_START` |140 m   |Begin tracking             |
|`RADAR_REPORT`|120 m   |Generate threat report     |
|`RADAR_LAUNCH`|110 m   |Authorize & launch SHEHANAH|

```python
if target_north <= RADAR_LAUNCH:
    print("🚀 Launch SHEHANAH")
```

### 2. Launch Phase

SHEHANAH runs a preflight GPS check, arms, activates offboard mode, and climbs to 50 m — 20 m above the target:

```python
await drone.action.arm()
await drone.offboard.start()
# Climbs to SHEHANAH_ALT = 50.0 m (target flies at 30.0 m)
```

### 3. Interception Phase

The drone tracks and closes in using a dynamic distance-reduction algorithm. At ≤ 15 m from the target, it dives to 31 m to match altitude:

```python
shehanah_north = move_towards(shehanah_north, target_north, FOLLOW_SPEED)
distance = abs(shehanah_north - target_north)

if distance <= 15.0:
    current_alt = 31.0  # Dive toward target altitude
```

### 4. Final Approach

When distance drops to ≤ 1 meter, interception is confirmed:

```python
if distance <= 1.0:
    print("🛰️ INTERCEPT CONFIRMED")
```

### 5. Mission End

System safely stops offboard control and disarms:

```python
await drone.offboard.stop()
await drone.action.disarm()
```

-----

## 🔄 System States

|State      |Description                                |
|-----------|-------------------------------------------|
|`WAIT`     |Monitoring airspace, awaiting radar trigger|
|`LAUNCH`   |Arming, offboard activation, takeoff       |
|`INTERCEPT`|Actively tracking and closing on target    |
|`END`      |Interception confirmed, mission complete   |

-----

## 🛠️ Tech Stack

|Component        |Technology          |
|-----------------|--------------------|
|Language         |Python              |
|Flight Control   |PX4 Autopilot       |
|UAV Communication|MAVSDK              |
|Autonomy         |Custom State Machine|

-----

## 📄 License

This project has been submitted to the **Saudi Authority for Intellectual Property (SAIP)** for patent registration.

-----

## 👤 Author

**SHEHANAH Project** — Built as a step toward intelligent drone systems and smart air defense.
