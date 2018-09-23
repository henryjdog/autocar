import RPi.GPIO as io
import time

io.setmode(io.BOARD)

fpin = 15
bpin = 16
lpin = 11
rpin = 13

pins = (fpin, bpin, lpin, rpin)

for pin in pins:
    io.setup(pin, io.OUT)

def init_pwm(pin):
    p = io.PWM(pin, 100)
    p.ChangeDutyCycle(0)
    p.start(100)
    p.ChangeDutyCycle(0)
    return p


fpwm = init_pwm(fpin)
bpwm = init_pwm(bpin)
lpwm = init_pwm(lpin)
rpwm = init_pwm(rpin)

def stop(pwms=[fpwm, lpwm, rpwm, bpwm]):
    for pwm in pwms:
        pwm.ChangeDutyCycle(0)

def f(pct=0.0):
    stop([fpwm, bpwm])
    fpwm.ChangeDutyCycle(pct*100)

def b(pct=0.0):
    stop([fpwm, bpwm])
    bpwm.ChangeDutyCycle(pct*100)

def l(pct=0.0):
    stop([lpwm, rpwm])
    lpwm.ChangeDutyCycle(pct*100)

def r(pct=0.0):
    stop([lpwm, rpwm])
    rpwm.ChangeDutyCycle(pct*100)

if __name__ == '__main__':
    f(0.5)
    time.sleep(0.5)
    r(0.5)
    time.sleep(0.5)
    b(0.5)
    time.sleep(0.5)
    l(0.5)
    time.sleep(0.5)
    stop()
    io.cleanup()
