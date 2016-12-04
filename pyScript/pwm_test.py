#!/usr/bin/python -*- coding: UTF-8 -*-
import time
import urllib2, urllib
import json
import RPi.GPIO as GPIO
import MySQLdb
import serial

GPIO.setmode(GPIO.BOARD)

MotorPinX = 12
MotorPinY = 33

GPIO.setup(MotorPinX, GPIO.OUT)
GPIO.setup(MotorPinY, GPIO.OUT)

pwm_motorX = GPIO.PWM(MotorPinX, 50)
pwm_motorY = GPIO.PWM(MotorPinY, 50)

pwm_motorY.start(7.25)

transDuty = lambda x: 7.25 - float(x) / 40 * 17

while True:
    a=input('please input a num: ')

    #dutyResultY = transDuty(a)
    print a
    pwm_motorY.ChangeDutyCycle(a) # 驅動Y軸馬達
