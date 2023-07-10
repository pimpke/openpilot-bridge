from multiprocessing.connection import Listener

import numpy as np

from cereal import log
from cereal import messaging


def get_float_list(a):
    return [float(x) for x in list(a)]


def create_modelv2_msg(control_dict):
    md = messaging.new_message('modelV2')

    md.modelV2.frameId = control_dict['frame_id']

    md.modelV2.position = log.XYZTData.new_message()
    md.modelV2.position.x = get_float_list(control_dict['position_x'])
    md.modelV2.position.y = get_float_list(control_dict['position_y'])
    md.modelV2.position.z = get_float_list(np.zeros_like(control_dict['position_x']))
    md.modelV2.position.t = get_float_list(control_dict['position_t'])

    md.modelV2.velocity = log.XYZTData.new_message()
    md.modelV2.velocity.x = get_float_list(control_dict['velocity_x'])
    md.modelV2.velocity.y = get_float_list(control_dict['velocity_y'])
    md.modelV2.velocity.z = get_float_list(np.zeros_like(control_dict['velocity_x']))
    md.modelV2.velocity.t = get_float_list(control_dict['position_t'])

    md.modelV2.orientation = log.XYZTData.new_message()
    md.modelV2.orientation.x = get_float_list(np.zeros_like(control_dict['orientation_z']))
    md.modelV2.orientation.y = get_float_list(np.zeros_like(control_dict['orientation_z']))
    md.modelV2.orientation.z = get_float_list(control_dict['orientation_z'])
    md.modelV2.orientation.t = get_float_list(control_dict['position_t'])

    md.modelV2.orientationRate = log.XYZTData.new_message()
    md.modelV2.orientationRate.x = get_float_list(np.zeros_like(control_dict['orientation_rate_z']))
    md.modelV2.orientationRate.y = get_float_list(np.zeros_like(control_dict['orientation_rate_z']))
    md.modelV2.orientationRate.z = get_float_list(control_dict['orientation_rate_z'])
    md.modelV2.orientationRate.t = get_float_list(control_dict['position_t'])

    return md


def main(port=6010):
    pm = messaging.PubMaster(['modelV2'])

    try:
        import pydevd_pycharm
        pydevd_pycharm.settrace('localhost', port=1237, stdoutToServer=True, stderrToServer=True, suspend=False)
    except ConnectionRefusedError:
        print('[Warning] Debugger on port 1237 not found. Continuing...')

    print(f'Listening for connections on port {port}...')
    listener = Listener(('localhost', port))

    frame_id = 0
    while True:
        recv_conn = listener.accept()
        print('Connection accepted from', listener.last_accepted)

        try:
            while True:
                control_dict = recv_conn.recv()
                print('Successful receive')

                frame_id += 1
                control_dict['frame_id'] = frame_id

                msg = create_modelv2_msg(control_dict)
                print('Sending a modelv2 msg...')
                pm.send('modelV2', msg)
                print('Successful send')

        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
