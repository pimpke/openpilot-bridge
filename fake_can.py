import os
import threading
import time

from cereal import messaging

from opendbc.can.packer import CANPacker
from selfdrive.boardd.boardd_api_impl import can_list_to_can_capnp

from selfdrive.car import crc8_pedal
from selfdrive.dbg import settrace


def can_function(pm, packer, idx):
    speed = 1
    angle = 2
    # cruise_button = 3
    # is_engaged = True

    msg = []

    # *** powertrain bus ***

    speed = speed * 3.6  # convert m/s to kph
    # msg.append(packer.make_can_msg("ENGINE_DATA", 0, {"XMISSION_SPEED": speed}, idx))
    msg.append(packer.make_can_msg("WHEEL_SPEED", 0, {
        "WHEEL_SPEED_F": speed,
        "WHEEL_SPEED_B": speed,
    }, -1))

    # msg.append(packer.make_can_msg("SCM_BUTTONS", 0, {"CRUISE_BUTTONS": cruise_button}, idx))

    # values = {"COUNTER_PEDAL": idx & 0xF}
    # checksum = crc8_pedal(packer.make_can_msg("GAS_SENSOR", 0, {"COUNTER_PEDAL": idx & 0xF}, -1)[2][:-1])
    # values["CHECKSUM_PEDAL"] = checksum
    # msg.append(packer.make_can_msg("GAS_SENSOR", 0, values, -1))

    # msg.append(packer.make_can_msg("GEARBOX", 0, {"GEAR": 4, "GEAR_SHIFTER": 8}, idx))
    # msg.append(packer.make_can_msg("GAS_PEDAL_2", 0, {}, idx))
    # msg.append(packer.make_can_msg("SEATBELT_STATUS", 0, {"SEATBELT_DRIVER_LATCHED": 1}, idx))
    # msg.append(packer.make_can_msg("STEER_STATUS", 0, {}, idx))
    msg.append(packer.make_can_msg("STEERING_ANGLE_SENSOR", 0, {"STEER_ANGLE": angle}, idx))
    msg.append(packer.make_can_msg("BRAKE", 0, {"BRAKE_PRESSURE": 2, "BRAKE_ENGAGED": 1}, idx))
    # msg.append(packer.make_can_msg("VSA_STATUS", 0, {}, idx))
    # msg.append(packer.make_can_msg("STANDSTILL", 0, {"WHEELS_MOVING": 1 if speed >= 1.0 else 0}, idx))
    # msg.append(packer.make_can_msg("STEER_MOTOR_TORQUE", 0, {}, idx))
    # msg.append(packer.make_can_msg("EPB_STATUS", 0, {}, idx))
    # msg.append(packer.make_can_msg("DOORS_STATUS", 0, {}, idx))
    # msg.append(packer.make_can_msg("CRUISE_PARAMS", 0, {}, idx))
    # msg.append(packer.make_can_msg("CRUISE", 0, {}, idx))
    # msg.append(packer.make_can_msg("SCM_FEEDBACK", 0, {"MAIN_ON": 1}, idx))
    # msg.append(packer.make_can_msg("POWERTRAIN_DATA", 0, {"ACC_STATUS": int(is_engaged)}, idx))
    # msg.append(packer.make_can_msg("HUD_SETTING", 0, {}))

    # *** cam bus ***
    # msg.append(packer.make_can_msg("STEERING_CONTROL", 2, {}, idx))
    # msg.append(packer.make_can_msg("ACC_HUD", 2, {}, idx))
    # msg.append(packer.make_can_msg("BRAKE_COMMAND", 2, {}, idx))

    pm.send('can', can_list_to_can_capnp(msg))


def can_function_runner(exit_event: threading.Event):
    pm = messaging.PubMaster(['can'])
    # packer = CANPacker("honda_civic_touring_2016_can_generated")
    packer = CANPacker("perodua_general_pt")
    i = 0
    while not exit_event.is_set():
        can_function(pm, packer, i)
        time.sleep(0.01)
        i += 1


def bridge():
    exit_event = threading.Event()
    threads = [threading.Thread(target=can_function_runner, args=(exit_event,))]

    for t in threads:
        t.start()

    for t in reversed(threads):
        t.join()


def bridge_keep_alive():
    while 1:
        try:
            bridge()
            break
        except RuntimeError:
            print("Restarting bridge...")


def main():
    try:
        if os.environ['DEBUG_FAKE_CAN'] == '1':
            settrace()
    except KeyError:
        pass

    bridge_keep_alive()


if __name__ == "__main__":
    main()
