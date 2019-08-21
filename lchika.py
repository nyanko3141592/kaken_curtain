#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
def gpio_write1(a):
    for x in range(3):
        if a!=0:
            GPIO.output(a,True)
            print('write')
        time.sleep(2)
        GPIO.output(a,False)
        time.sleep(2)
    GPIO.cleanup()
    
def gpio_write2(a,b):
    for x in range(3):
        if a!=0 and b !=0:
            GPIO.output(a,True)
            GPIO.output(b,True)
            print('write')
        time.sleep(2)
        GPIO.output(a,False)
        GPIO.output(b,False)
        time.sleep(2)
    GPIO.cleanup()
    
if __name__ == "__main__":
    gpio_write2(2,3)
