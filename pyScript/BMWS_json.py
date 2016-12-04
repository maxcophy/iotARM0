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

pwm_motorX.start(7.25)
pwm_motorY.start(7.25)

transDuty = lambda x: 7.25 - float(x) / 40 * 17

host = 'localhost'  # 更改主機位置
url = 'http://%s/iotARM/phpFunction/json_iot.php' % host
updateURL = 'http://%s/iotARM/phpFunction/update_iot.php?' % host

def motorMov(flag, argX, argY, update='', movSet=0.5):
    ''' 函數帶入5個引數
            flag: 'u','r','d','l','web'
            argX,argY: 為資料庫的x,y座標
            update: 更改資料庫的網址,預設為空值
            movSet: 馬達的步進值,預設為0.5

        函數返回
            返回updatet字串,串接get參數字串
    '''
    # 判斷藍芽案的按鈕---start---
    if flag == 'u' or flag == 'r':  # 如果按上或右
        if flag == 'u':
            argY += movSet
            update += 'move=up'
        elif flag == 'r':
            argX += movSet
            update += 'move=right'

    elif flag == 'd' or flag == 'l':  # 按下或左
        if flag == 'd':
            argY += -movSet
            update += 'move=down'
        elif flag == 'l':
            argX += -movSet
            update += 'move=left'
    # 判斷藍芽案的按鈕---end---

    else:   # 若藍芽沒動則Web動
        global isYMov
        # 判斷Web的按鈕並驅動馬達---start---
        if isYMov: 
            dutyResultY = round(transDuty(argY),2) # 四捨五入小數點第二位
            print 'Web Y軸dutyCycle: '+str(dutyResultY)
            pwm_motorY.ChangeDutyCycle(dutyResultY) # 驅動Y軸馬達
        else:
            dutyResultX = round(transDuty(argX),2)
            print 'Web X軸dutyCycle: '+str(dutyResultX)
            pwm_motorX.ChangeDutyCycle(dutyResultX) # 驅動Y軸馬達
        
        update += 'move=web'
        print '執行的網址: '+update
        return update
        # 判斷web的按鈕並驅動馬達---end---

    if (argY - resultY) != 0:
        dutyResultY = round(transDuty(argY),2)  # 將Y座標轉換為DutyCycle
        print 'BT Y軸dutyCycle: '+str(dutyResultY)
        pwm_motorY.ChangeDutyCycle(dutyResultY)
    else:
        dutyResultX = round(transDuty(argX)) # 將X座標轉換為DutyCycle
        print 'BT X軸dutyCycle: '+str(dutyResultX)
        pwm_motorX.ChangeDutyCycle(dutyResultX)
    time.sleep(0.25)
    
    print '執行的網址: '+update
    return update

def execURL(url, feedback=False):
    ''' 函數帶入兩個引數
            url: 要執行的網址
            feedback: 是否要回傳資料庫轉json的格式,預設不回傳

        函數返回
            返回一個5個值的Tuple
    '''
    urlFp = urllib2.urlopen(url) # 要求網址

    if feedback:
        dData = json.load(urlFp) # 將response轉換為json
        dData['isMov'] = (False, True)[dData['isMov'] == '1']   # 將返回的json '1'轉為True '0'轉為False
        dData['isXMov'] = (False, True)[dData['isXMov'] == '1']
        dData['isYMov'] = (False, True)[dData['isYMov'] == '1']
        urlFp.close()
        
        print (float(dData['movX']), float(dData['movY']), dData['isMov'],dData['isXMov'],dData['isYMov'])
        return (float(dData['movX']), float(dData['movY']), dData['isMov'],dData['isXMov'],dData['isYMov'])
    
    urlFp.close()

while True:
        while True:
            try:
                resultX, resultY, isMov, isXMov, isYMov = execURL(url, True)  # 設定變數初始值
            except:
                print 'Get DBData failed, retry Now!'
                time.sleep(2)
            else:
                break

        #ser = serial.Serial("/dev/serial0", 9600, timeout=0.5)
        #command = ser.read()  # 讀取藍芽阜的值
        command = False
        #print command
        # if-判斷藍牙是否送值,有值才繼續執行藍牙操作
        if command:
            print "BT"
            # 藍牙操作---start---
            execUpdateURL = motorMov(command, resultX, resultY, updateURL)
            execURL(execUpdateURL)
            # 藍牙操作---end---

        elif isMov:
            print 'web'
            # Web操作---start---
            execUpdateURL = motorMov('web', resultX, resultY, updateURL)
            execURL(execUpdateURL)
            # Web操作---end---

        else:
            print "未連接"
        time.sleep(0.25) 

GPIO.cleanup()
