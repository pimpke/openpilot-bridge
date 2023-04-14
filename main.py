import copy
import os
import time
from collections import defaultdict
from multiprocessing.connection import Client

from selfdrive.boardd.boardd_api_impl import can_list_to_can_capnp

from cereal import messaging
from opendbc.can.parser import CANParser
from selfdrive.boardd.boardd import can_capnp_to_can_list
from selfdrive.dbg import settrace


def update_parser(parser, msgs):
    bts = can_list_to_can_capnp(msgs)
    parser.update_string(bts)


def main():
    try:
        if os.environ['DEBUG_OPENPILOT_BRIDGE'] == '1':
            settrace()
    except KeyError:
        pass

    dbc_file = "honda_civic_touring_2016_can_generated"

    signals = [
        ("XMISSION_SPEED", "ENGINE_DATA"),
        ("STEER_ANGLE", "STEERING_SENSORS"),
        ("WHEEL_SPEED_FL", "WHEEL_SPEEDS"),
        ("WHEEL_SPEED_FR", "WHEEL_SPEEDS"),
        ("WHEEL_SPEED_RL", "WHEEL_SPEEDS"),
        ("WHEEL_SPEED_RR", "WHEEL_SPEEDS")
    ]
    checks = [("ENGINE_DATA", 100),
              ("STEERING_SENSORS", 100),
              ("WHEEL_SPEEDS", 50)]

    parser = CANParser(dbc_file, copy.deepcopy(signals), copy.deepcopy(checks), 0)

    print('Connecting to localhost:7777...')
    while True:
        try:
            send_conn = Client(('localhost', 7777))
            break
        except ConnectionRefusedError:
            time.sleep(0.1)
    print('Connected to localhost:7777!')

    msg_name_to_signal_names = defaultdict(list)
    for s in signals:
        msg_name_to_signal_names[s[1]].append(s[0])

    msg_name_to_last_tstamp = {c[0]: None for c in checks}

    sm = messaging.SubMaster(['can'])
    while 1:
        sm.update()
        update_parser(parser, can_capnp_to_can_list(sm['can']))

        for msg_name in msg_name_to_last_tstamp:
            parsed_msg_tstamp = parser.ts_nanos[msg_name]['CHECKSUM']

            for key in parser.ts_nanos[msg_name]:
                assert parser.ts_nanos[msg_name][key] == parsed_msg_tstamp

            if msg_name_to_last_tstamp[msg_name] != parsed_msg_tstamp:
                msg_name_to_last_tstamp[msg_name] = parsed_msg_tstamp

                msg = {
                    'msg_name': msg_name,
                    'log_mono_timestamp': parsed_msg_tstamp,
                    'signals': {
                        signal_name:
                            parser.vl[msg_name][signal_name] for signal_name in msg_name_to_signal_names[msg_name]
                    }
                }

                send_conn.send(msg)


if __name__ == '__main__':
    main()
