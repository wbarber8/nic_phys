#import RPi.GPIO as GPIO
# import the python pigpio bindings
import pigpio
import time
pi = pigpio.pi()
pi.set_mode(21, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)
pi.set_mode(25, pigpio.OUTPUT)
pi.set_mode(27, pigpio.OUTPUT)

pi.set_mode(20, pigpio.INPUT)
pi.set_mode(22, pigpio.INPUT)
pi.set_mode(24, pigpio.INPUT)
pi.set_mode(26, pigpio.INPUT)

count = 1

while count < 10:
    pi.write(23, 0)
    time.sleep(1)
    pi.write(23,1)
    time.sleep(1)
    count = count + 1
