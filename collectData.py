# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 23:10:00 2021

@author: Musya
"""

import cv2
import sys
import os
import pygame as pg
import time
from motorControl import Motor
from csvfile import writeCsv
from datetime import datetime

os.chdir('/home/pi/Autonomous-Car/')
if os.path.exists('/home/pi/Autonomous-Car/DATA'):
    os.chdir('/home/pi/Autonomous-Car/DATA')
else:
    os.mkdir('DATA')
    os.chdir('/home/pi/Autonomous-Car/DATA')
if os.path.exists('/home/pi/Autonomous-Car/DATA/IMG'):
    os.chdir('IMG')
else:
    os.mkdir('IMG')
    os.chdir('/home/pi/Autonomous-Car/DATA/IMG')

path = os.getcwd()
print(datetime.now())
print(path)
PWML,PWMR = 8,8
cap = cv2.VideoCapture(0)

images = []
steering =  []
throttle = []
def captureData():
    step = 0.5
    motor_left  = Motor(26,20,21)#EN,IN1,IN2
    motor_right = Motor(19,12,16)#EN,IN3,IN4
    global PWML
    global PWMR
    record = False
    pg.display.set_caption("ACAR")
    screen = pg.display.set_mode([450,450])
    while True:
        for eve in pg.event.get():pass
        key = pg.key.get_pressed()
        if key [pg.K_UP]:
            PWML = PWML + step
            PWMR = PWMR + step

        if key [pg.K_DOWN]:
            PWML = PWML - step
            PWMR = PWMR - step

        if key [pg.K_LEFT]:
            PWML = PWML - step
            PWMR = PWMR + step

        if key [pg.K_RIGHT]:
            PWMR = PWMR - step
            PWML = PWML + step
        if key [pg.K_SPACE]:
            record = True

        if key [pg.K_END]:
            record = False

        if PWML < 5:
            PWML = 5
        elif PWML > 80:
            PWML = 80
        if PWMR < 5:
            PWMR = 5
        elif PWMR > 80:
            PWMR = 80
        motor_left.forwardL(PWML,0)
        motor_right.forwardR(PWMR,0)


        name = str(datetime.now())+'.jpeg'
        name = str(os.path.join(path,name))




        pg.display.update()

        _,frame = cap.read()
        cv2.imshow("frame",frame)

        if record:
            print("Recording...", PWML,PWMR)
            cv2.imwrite(name,frame)
            images.append(name)
            steering.append(PWML)
            throttle.append(PWMR)
        else:
            print("Not Recording", PWML,PWMR)
            pass

        #time.sleep(0.0001)

        if cv2.waitKey(1) == ord('q'):
            break

    writeCsv(images, steering, throttle)

captureData()