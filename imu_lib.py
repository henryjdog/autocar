#!/usr/bin/env python
# coding: utf-8

import datetime as dt
#import ctypes
from ctypes import *


path = "../LSM9DS1_RaspberryPi_Library/lib/liblsm9ds1cwrapper.so"
lib = cdll.LoadLibrary(path)

lib.lsm9ds1_create.argtypes = []
lib.lsm9ds1_create.restype = c_void_p

lib.lsm9ds1_begin.argtypes = [c_void_p]
lib.lsm9ds1_begin.restype = None

lib.lsm9ds1_calibrate.argtypes = [c_void_p]
lib.lsm9ds1_calibrate.restype = None

lib.lsm9ds1_gyroAvailable.argtypes = [c_void_p]
lib.lsm9ds1_gyroAvailable.restype = c_int
lib.lsm9ds1_accelAvailable.argtypes = [c_void_p]
lib.lsm9ds1_accelAvailable.restype = c_int
lib.lsm9ds1_magAvailable.argtypes = [c_void_p]
lib.lsm9ds1_magAvailable.restype = c_int

lib.lsm9ds1_readGyro.argtypes = [c_void_p]
lib.lsm9ds1_readGyro.restype = c_int
lib.lsm9ds1_readAccel.argtypes = [c_void_p]
lib.lsm9ds1_readAccel.restype = c_int
lib.lsm9ds1_readMag.argtypes = [c_void_p]
lib.lsm9ds1_readMag.restype = c_int

lib.lsm9ds1_getGyroX.argtypes = [c_void_p]
lib.lsm9ds1_getGyroX.restype = c_float
lib.lsm9ds1_getGyroY.argtypes = [c_void_p]
lib.lsm9ds1_getGyroY.restype = c_float
lib.lsm9ds1_getGyroZ.argtypes = [c_void_p]
lib.lsm9ds1_getGyroZ.restype = c_float

lib.lsm9ds1_getAccelX.argtypes = [c_void_p]
lib.lsm9ds1_getAccelX.restype = c_float
lib.lsm9ds1_getAccelY.argtypes = [c_void_p]
lib.lsm9ds1_getAccelY.restype = c_float
lib.lsm9ds1_getAccelZ.argtypes = [c_void_p]
lib.lsm9ds1_getAccelZ.restype = c_float

lib.lsm9ds1_getMagX.argtypes = [c_void_p]
lib.lsm9ds1_getMagX.restype = c_float
lib.lsm9ds1_getMagY.argtypes = [c_void_p]
lib.lsm9ds1_getMagY.restype = c_float
lib.lsm9ds1_getMagZ.argtypes = [c_void_p]
lib.lsm9ds1_getMagZ.restype = c_float

lib.lsm9ds1_calcGyro.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcGyro.restype = c_float
lib.lsm9ds1_calcAccel.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcAccel.restype = c_float
lib.lsm9ds1_calcMag.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcMag.restype = c_float

class IMU():
    self.last_read_time = 0
    
    def __init__(self):
        self.imu = lib.lsm9ds1_create()
        lib.lsm9ds1_begin(self.imu)
        if lib.lsm9ds1_begin(self.imu) == 0:
            print("Failed to communicate with LSM9DS1.")
            quit()
        lib.lsm9ds1_calibrate(self.imu)

    def read(self):
        while lib.lsm9ds1_gyroAvailable(self.imu) == 0:
            pass
        lib.lsm9ds1_readGyro(self.imu)
        while lib.lsm9ds1_accelAvailable(self.imu) == 0:
            pass
        lib.lsm9ds1_readAccel(self.imu)
        while lib.lsm9ds1_magAvailable(self.imu) == 0:
            pass
        lib.lsm9ds1_readMag(self.imu)

        gx = lib.lsm9ds1_getGyroX(self.imu)
        gy = lib.lsm9ds1_getGyroY(self.imu)
        gz = lib.lsm9ds1_getGyroZ(self.imu)
        
        ax = lib.lsm9ds1_getAccelX(self.imu)
        ay = lib.lsm9ds1_getAccelY(self.imu)
        az = lib.lsm9ds1_getAccelZ(self.imu)

        mx = lib.lsm9ds1_getMagX(self.imu)
        my = lib.lsm9ds1_getMagY(self.imu)
        mz = lib.lsm9ds1_getMagZ(self.imu)

        cgx = lib.lsm9ds1_calcGyro(self.imu, gx)
        cgy = lib.lsm9ds1_calcGyro(self.imu, gy)
        cgz = lib.lsm9ds1_calcGyro(self.imu, gz)
        self.gyro = (cgx, cgy, cgz)
        
        cax = lib.lsm9ds1_calcAccel(self.imu, ax)
        cay = lib.lsm9ds1_calcAccel(self.imu, ay)
        caz = lib.lsm9ds1_calcAccel(self.imu, az)
        self.accel = (cax, cay, caz)
        
        cmx = lib.lsm9ds1_calcMag(self.imu, mx)
        cmy = lib.lsm9ds1_calcMag(self.imu, my)
        cmz = lib.lsm9ds1_calcMag(self.imu, mz)
        self.mag = (cmx, cmy, cmz)

        self.last_read_time = dt.datetime.now()