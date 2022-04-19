import RPi.GPIO as GPIO
import time

ENA = 26
ENB = 19
IN1 = 20
IN2 = 21
IN3 = 12
IN4 = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor:
    def __init__(self,ENA,IN1,IN2):
        self.ENA = ENA
        self.IN1 = IN1
        self.IN2 = IN2
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)

        self.pwm = GPIO.PWM(self.ENA,100)
        self.pwm.start(0)

    def forwardL(self,PWM,delay):
        GPIO.output(self.IN1,GPIO.LOW)
        GPIO.output(self.IN2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(PWM)
        time.sleep(delay)
    def forwardR(self,PWM,delay):
        GPIO.output(self.IN1,GPIO.HIGH)
        GPIO.output(self.IN2,GPIO.LOW)
        self.pwm.ChangeDutyCycle(PWM)
        time.sleep(delay)

if __name__ == '__main__':
    motor_left  = Motor(26,20,21)#EN,IN1,IN2
    motor_right = Motor(19,12,16)#EN,IN3,IN4
    while True:
        print("Looping...")
        motor_left.forwardL(45,0)
        motor_right.forwardR(45,0)
    GPIO.cleanup()