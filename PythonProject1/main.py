import asyncio
from mavsdk import System
from mavsdk.offboard import PositionNedYaw

# =========================
# CONFIG
# =========================

RADAR_START = 140.0
RADAR_REPORT = 120.0
RADAR_LAUNCH = 110.0

TARGET_ALT = 30.0
TARGET_SPEED = 1.0

SHEHANAH_ALT = 50.0
FOLLOW_SPEED = 2.5

# =========================
# STATES
# =========================

WAIT = "WAIT"
LAUNCH = "LAUNCH"
INTERCEPT = "INTERCEPT"
END = "END"

# =========================
# HELPERS
# =========================

def move_towards(current, target, step):
    if current < target:
        return min(current + step, target)
    return max(current - step, target)


async def safe_arm(drone):
    print("🔧 Preflight check...")

    async for h in drone.telemetry.health():
        if h.is_global_position_ok and h.is_home_position_ok:
            print("✅ GPS OK")
            break

    for i in range(3):
        try:
            print(f"🔐 ARM attempt {i+1}")
            await drone.action.arm()
            print("✅ Armed")
            return True
        except Exception as e:
            print(f"⚠️ ARM failed: {e}")
            await asyncio.sleep(1)

    return False


# =========================
# MAIN
# =========================

async def main():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("\n📡 SHEHANAH RADAR SYSTEM ONLINE")
    await asyncio.sleep(1)

    print("🛰️ Monitoring airspace...\n")
    await asyncio.sleep(1)

    # =========================
    # INITIAL VALUES
    # =========================

    target_north = RADAR_START
    shehanah_north = 0.0
    yaw = 0
    state = WAIT
    report_shown = False

    # =========================
    # CONNECT TO PX4
    # =========================

    async for c in drone.core.connection_state():
        if c.is_connected:
            print("✅ Connected to PX4\n")
            break

    async for h in drone.telemetry.health():
        if h.is_global_position_ok:
            print("📡 GPS Locked\n")
            break

    # =========================
    # MAIN LOOP
    # =========================

    while True:

        await asyncio.sleep(0.5)

        target_north -= TARGET_SPEED

        # =========================
        # WAIT STATE
        # =========================

        if state == WAIT:

            print(f"\n📡 Target approaching | Distance: {target_north:.1f} m")
            await asyncio.sleep(1)

            if target_north <= RADAR_REPORT and not report_shown:

                report_shown = True

                print("🚨 RADAR STATUS REPORT")
                await asyncio.sleep(1)

                print("🛸 Unidentified drone detected inside protected airspace")
                await asyncio.sleep(1)

                print(f"📍 Current position: {target_north:.1f} m from border entry")
                await asyncio.sleep(1)

                print(f"📈 Altitude: {TARGET_ALT:.0f} m")
                await asyncio.sleep(1)

                print("⚡ Speed: 30 km/h")
                await asyncio.sleep(1)

                print("🧭 Direction: North → South")
                await asyncio.sleep(1)

                print("📡 Threat assessment: Active tracking confirmed")
                await asyncio.sleep(1)

                print("🛰️ SHEHANAH on standby")
                await asyncio.sleep(1)

            if target_north <= RADAR_LAUNCH:

                print("\n🚨 ALERT: 110m REACHED")
                await asyncio.sleep(1)

                print("📡 Target entered engagement zone")
                await asyncio.sleep(1)

                print("🛰️ SHEHANAH AUTHORIZED")
                await asyncio.sleep(1)

                print("🚀 Launch SHEHANAH")
                await asyncio.sleep(1)

                ok = await safe_arm(drone)
                if not ok:
                    print("❌ Mission aborted")
                    return

                await drone.offboard.set_position_ned(
                    PositionNedYaw(0.0, 0.0, -10.0, 0.0)
                )
                await drone.offboard.start()

                shehanah_north = 0.0
                state = LAUNCH

        # =========================
        # LAUNCH STATE
        # =========================

        elif state == LAUNCH:

            print("\n🚁 SHEHANAH TAKING POSITION")
            await asyncio.sleep(1)

            print("📈 Target Altitude: 30 m")
            await asyncio.sleep(1)

            print("📈 SHEHANAH Altitude: 50 m (+20 m advantage)")
            await asyncio.sleep(1)

            print("⚡ Target Speed: 30 km/h")
            await asyncio.sleep(1)

            print("⚡ SHEHANAH Speed: 60 km/h")
            await asyncio.sleep(1)

            await drone.offboard.set_position_ned(
                PositionNedYaw(
                    shehanah_north,
                    0.0,
                    -SHEHANAH_ALT,
                    yaw
                )
            )

            await asyncio.sleep(2)

            state = INTERCEPT

        # =========================
        # INTERCEPT STATE
        # =========================

        elif state == INTERCEPT:

            target_north -= TARGET_SPEED

            shehanah_north = move_towards(
                shehanah_north,
                target_north,
                FOLLOW_SPEED
            )

            distance = abs(shehanah_north - target_north)

            current_alt = SHEHANAH_ALT

            if distance <= 15.0:
                current_alt = 31.0

            await drone.offboard.set_position_ned(
                PositionNedYaw(
                    shehanah_north,
                    0.0,
                    -current_alt,
                    yaw
                )
            )

            print("\n📡 INTERCEPT HUD")
            print(f"📍 Target Position: {target_north:.2f} m")
            print(f"🚁 SHEHANAH Position: {shehanah_north:.2f} m")
            print(f"🎯 Distance to Target: {distance:.2f} m")
            print(f"📈 Target Altitude: {TARGET_ALT:.0f} m")
            print(f"📈 SHEHANAH Altitude: {current_alt:.0f} m")

            if current_alt == 31.0:
                print("🦅 STATUS: Diving toward target")
            else:
                print("📡 STATUS: Closing in")

            print("--------------------------------------------------")

            await asyncio.sleep(1)

            if distance <= 1.0:

                target_north = shehanah_north

                print("\n📡 FINAL APPROACH")
                print(f"📍 Target Position: {target_north:.2f} m")
                print(f"🚁 SHEHANAH Position: {shehanah_north:.2f} m")
                print("🎯 Distance to Target: 1.00 m")
                print("📈 Target Altitude: 30 m")
                print("📈 SHEHANAH Altitude: 31 m")
                print("🦅 STATUS: Contact imminent")
                print("--------------------------------------------------")

                await asyncio.sleep(1)

                print("\n🛰️ INTERCEPT CONFIRMED")
                await asyncio.sleep(1)

                print("📡 Interception confirmed by SHEHANAH")

                state = END

        # =========================
        # END STATE
        # =========================

        elif state == END:

            print("\n💥 SYSTEM SHUTDOWN")
            await asyncio.sleep(1)

            print("📡 Stopping flight control")
            await asyncio.sleep(1)

            print("🛑 Disarming motors")
            await asyncio.sleep(1)

            try:
                await drone.offboard.stop()
            except:
                pass

            try:
                await drone.action.disarm()
            except:
                pass

            print("\n📁 Mission Complete")
            print("🛰️ SHEHANAH successful interception")

            break


if __name__ == "__main__":
    asyncio.run(main())
