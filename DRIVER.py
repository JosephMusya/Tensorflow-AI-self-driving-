from motorControl import Motor
import tensorflow as tf
import cv2
import numpy as np

PWML,PWMR = 12,12
motor_left  = Motor(26,20,21)#EN,IN1,IN2
motor_right = Motor(19,12,16)#EN,IN3,IN4

cap = cv2.VideoCapture(0)
model = tf.keras.models.load_model('/home/pi/Autonomous-Car/driver_version_1.2.h5')
while True:
    _,frame = cap.read()
    cv2.imshow("Frame",frame)
    img = cv2.resize(frame,(200,66))/255.0

    img = np.array(img)
    img = np.reshape(img,(1,66,200,3))
    PWM = model.predict(img)

    frame = cv2.resize(frame,(320,240))

    PWML = PWM[0]*1.5
    PWMR = PWM[1]*1.5
    if PWML < 5:
        PWML =5
    if PWMR < 5:
        PWMR = 5
    motor_left.forwardL(PWML,0)
    motor_right.forwardR(PWMR,0)
    print(PWML,PWMR)
    if cv2.waitKey(1) == ord('q'):
        break


motor_left.forwardL(PWML,0)
motor_right.forwardR(PWMR,0)