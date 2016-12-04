#!/usr/bin/python -*- coding: UTF-8 -*-
import time
import RPi.GPIO as GPIO
import MySQLdb
import serial

GPIO.setmode(GPIO.BOARD)

MotorPinX = 33
MotorPinY = 12


GPIO.setup(MotorPinX, GPIO.OUT)
GPIO.setup(MotorPinY, GPIO.OUT)

pwm_motorX = GPIO.PWM(MotorPinX, 50)
pwm_motorY = GPIO.PWM(MotorPinY, 50)

pwm_motorX.start(4)
pwm_motorY.start(4)


while True:
        db = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="iot")  # mysql連線
        cursor = db.cursor()  # 取得資料游標
        cursor.execute("SELECT `movX`,`movY`,`isBTMove`,`isWebMove` FROM `action` WHERE 1")  # 執行SQL語法
        result = cursor.fetchone()  # 取得一筆資料

        resultX = result[0]  # 設定X數值
        resultY = result[1]  # 設定Y數值
        isBTMove = result[2]
        isWebMove = result[3]

        print "BT X:", resultX
        print "BT Y:", resultY
        ser = serial.Serial("/dev/serial0", 9600, timeout=0.5)
        command = ser.read()  # 讀取藍芽阜的值
        ###if-判斷藍牙是否送值,有值才繼續執行藍牙操作
        if command:
                
            ###藍牙操作---start---
        	if command == 'u':
                    print "up"
                    if resultY <= 9.5:
                        print resultY
                        resultY = resultY + 0.5
                        print resultY
                        dutyResultY = 7.25 - float(resultY) / 40 * 17  # 將Y座標轉換為DutyCycle
                        print 'dutyResultY='+str(dutyResultY)
                        pwm_motorY.ChangeDutyCycle(dutyResultY)
                        time.sleep(0.5)

                        sql="UPDATE `iot`.`action` SET `movX` ='"+str(resultX)+"', `movY` = '"+str(resultY)+"' WHERE `action`.`id` = 1"
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rolback()
                        cursor.close()
		elif command == 'd':
                    print "down"
                    if resultY >= -9.5:
                        print resultY
                        resultY = resultY - 0.5
                        print resultY
                        dutyResultY = 7.25 - float(resultY) / 40 * 17  # 將Y座標轉換為DutyCycle
                        print 'dutyResultY='+str(dutyResultY)
                        pwm_motorY.ChangeDutyCycle(dutyResultY)
                        time.sleep(0.5)

                        sql="UPDATE `iot`.`action` SET `movX` ='"+str(resultX)+"', `movY` = '"+str(resultY)+"' WHERE `action`.`id` = 1"
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rolback()
                        cursor.close()
		elif command == 'r':
                    print "right"
                    if resultX <= 9.5:
                        print resultX
                        resultX = resultX + 0.5
                        print resultX
                        dutyResultX = 7.25 - float(resultX) / 40 * 17  # 將Y座標轉換為DutyCycle
                        print 'dutyResultX='+str(dutyResultX)
                        pwm_motorX.ChangeDutyCycle(dutyResultX)
                        time.sleep(0.5)

                        sql="UPDATE `iot`.`action` SET `movX` ='"+str(resultX)+"', `movY` = '"+str(resultY)+"' WHERE `action`.`id` = 1"
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rolback()
                        cursor.close()
		elif command == 'l':
                    print "left"
                    if resultX >= -9.5:
                        print resultX
                        resultX = resultX - 0.5
                        print resultX
                        dutyResultX = 7.25 - float(resultX) / 40 * 17  # 將Y座標轉換為DutyCycle
                        print 'dutyResultX='+str(dutyResultX)
                        pwm_motorX.ChangeDutyCycle(dutyResultX)
                        time.sleep(0.5)

                        sql="UPDATE `iot`.`action` SET `movX` ='"+str(resultX)+"', `movY` = '"+str(resultY)+"' WHERE `action`.`id` = 1"
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rolback()
                        cursor.close()
                   ###藍牙操作---end---
        elif isWebMove==1:
                cursor = db.cursor()  # 取得資料游標
                cursor.execute("SELECT `movX`,`movY` FROM `action` WHERE 1")  # 執行SQL語法

                result = cursor.fetchone()  # 取得一筆資料

                movX = 7.25 - float(resultX) / 40 * 17  # 將X座標轉換為DutyCycle
                movY = 7.25 - float(resultY) / 40 * 17  # 將Y座標轉換為DutyCycle

                print "DutyCycleX:", movX
                print "DutyCycleY:", movY

                pwm_motorX.ChangeDutyCycle(movX)  # 驅動馬達X轉向
                pwm_motorY.ChangeDutyCycle(movY)  # 驅動馬達Y轉向
                time.sleep(0.5)

                sql2="UPDATE `action` SET `isWebMove` = 0 WHERE `action`.`id` = 1"
               # UPDATE `iot`.`action` SET `movX` = '3', `movY` = '3'WHERE `action`.`id` = 1;'
                cursor.execute(sql2)
                db.commit()
                cursor.close()
               ###MySQL動作---end---
        else:
            print "未連接"

