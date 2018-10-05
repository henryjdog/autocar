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

acc_x = []
acc_y = []
acc_z = []

speed_x = 0.0
speed_y = 0.0
speed_z = 0.0

# Main event loop
while True:
    acc_x_value, acc_y_value, acc_z_value = imu.read()[3:6]
    if len(acc_x) == 0:
        acc_x_init = acc_x_value
        acc_y_init = acc_y_value
        acc_z_init = acc_z_value

    acc_x.append(acc_x_value - acc_x_init)
    acc_y.append(acc_y_value - acc_y_init)
    acc_z.append(acc_z_value - acc_z_init)
    
    acc_x_read = sum(acc_x[:-3])/3
    acc_y_read = sum(acc_y[:-3])/3
    acc_z_read = sum(acc_z[:-3])/3

    speed_x = speed_x + acc_x_read*0.5
    print(acc_x)
    print(speed_x)
    
	command = raw_input('enter command')
	if command == 's':
		stop()
	elif command == 'f':
		f(0.2)
	elif command == 'b':
		b(0.2)
	elif command == 'l':
		l(0.8)
	elif command = 'r':
		r(0.8)
    

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

        
