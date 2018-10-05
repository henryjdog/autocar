# released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array
from time import sleep
from fcntl import ioctl
import motors
from imu import IMU
from controller import Controller

imu = IMU()
try:
    controller = Controller()
except:
    controller = None

# Main event loop
while True:
    print(imu.read())
    sleep(0.5)
    
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

        
