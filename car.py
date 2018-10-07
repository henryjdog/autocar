# released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array
import pandas as pd
from time import sleep
from fcntl import ioctl
from motors import *
import imu_lib
from controller import Controller

imu = imu_lib.IMU()
try:
    controller = Controller()
except:
    controller = None

acc_x = []
acc_y = []
acc_z = []

speed_x = 0.0
speed_y = 0.0
speed_z = 0.0

columns=['ts', 'gyro_x', 'gyro_y', 'gyro_z', 'acc_x', 'acc_y', 'acc_z', 'mag_x', 'mag_y', 'mag_z']
car_df = pd.DataFrame(columns=columns)

imu.read()
car_df = car_df.append(dict(zip(columns, imu.meas)), ignore_index=True)

mode = 'auto'
# Main event loop
while True:
    imu.read()
    car_df = car_df.append(dict(zip(columns, imu.meas)))

    if mode[:3] == 'man':
        command = raw_input('enter command')
        if command == 's':
            stop()
        elif command == 'f':
            f(0.4)
            print('forward')
        elif command == 'b':
            b(0.4)
            print('backward')
        elif command == 'l':
            l(0.5)
            print('left')
        elif command == 'r':
            r(0.5)
            print('right')
        elif command == 'straight':
            l()
            r()
            print('straight')


    if controller:
        evbuf = jsdev.read(8)
        if evbuf:
            time, value, type, number = struct.unpack('IhBB', evbuf)

            if type & 0x80:
                 print("(initial)",)

            if type & 0x01:
                button = button_map[number]
                if button:
                    button_states[button] = value
                    if value:
                        print("%s pressed" % (button))
                    else:
                        print("%s released" % (button))

            if type & 0x02:
                axis = axis_map[number]
                if axis:
                    fvalue = value / 32767.0
                    axis_states[axis] = fvalue
                    print("%s: %.3f" % (axis, fvalue))
                    if axis == 'x' or axis == 'hat0x':
                        if fvalue > 0.01:
                            r(fvalue)
                        elif fvalue < -0.01:
                            l(-fvalue)
                        else:
                            stop([lpwm, rpwm])
                    if axis == 'y' or axis == 'hat0y':
                        if fvalue < -0.01:
                            f(-fvalue)
                        elif fvalue > 0.01:
                            b(fvalue)
                        else:
                            stop([fpwm, bpwm])

        
