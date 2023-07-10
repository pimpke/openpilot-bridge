import time

import psutil


def find_and_kill_carla():
    for proc in psutil.process_iter():
        try:
            carla_sh = list(filter(lambda c: c.name() == 'CarlaUE4.sh', proc.children()))
            if len(carla_sh) > 0:
                assert len(carla_sh) == 1
                carla_sh = carla_sh[0]

                assert len(carla_sh.children()) == 1
                carla_bin = carla_sh.children()[0]

                assert carla_bin.name() == 'CarlaUE4-Linux-Shipping'

                carla_bin.kill()
                carla_sh.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


while True:
    if psutil.virtual_memory().percent >= 95:
        find_and_kill_carla()

    time.sleep(0.1)
