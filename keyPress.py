import pygame as pg
import time
from motorControl import Motor
#from collectData import captureData
PWML,PWMR = 10,10
def speed():
    motor_left  = Motor(26,20,21)#EN,IN1,IN2
    motor_right = Motor(19,12,16)#EN,IN3,IN4
    global PWML
    global PWMR
    global PWM
    pg.display.set_caption("ACAR")
    screen = pg.display.set_mode([450,450])
    while True:
        for eve in pg.event.get():pass
        key = pg.key.get_pressed()
        if key [pg.K_UP]:
            PWML = PWML + 1
            PWMR = PWMR + 1

        if key [pg.K_DOWN]:
            PWML = PWML - 1
            PWMR = PWMR - 1

        if key [pg.K_LEFT]:
            PWML = PWML - 1
            PWMR = PWMR + 1

        if key [pg.K_RIGHT]:
            PWMR = PWMR - 1
            PWML = PWML + 1
        captureData(PWML,PWMR)
        motor_left.forwardL(PWML,0)
        motor_right.forwardR(PWMR,0)

        print("PWM LEFT: ",PWML)
        print("PWM RIGHT: ",PWMR)

        time.sleep(0.1)
        pg.display.update()

if __name__ == "__main__":
    speed()