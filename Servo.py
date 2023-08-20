from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#servo pins
minPW=0.0004
maxPW=0.004

servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)

def Water():
    default = -0.3
    delay = 0.333
    servo.value = default
    sleep(2)
    
    for i in range(5):
        servo.value = -1
        sleep(delay)
        servo.value = default
        sleep(delay)

def Bubbles():
    default = -1
    delay1 = 1
    delay2 = 2
    servo.value = default
    sleep(2)

    for i in range(5):
        servo.value = 1
        sleep(delay1)
        servo.value = default
        sleep(delay1)

    for i in range(5):
        servo.value = 1
        sleep(delay2)
        servo.value = default
        sleep(delay2)
    

try:
    Water()

finally:
    GPIO.cleanup()