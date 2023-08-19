from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)

#servo pins
minPW=0.001
maxPW=0.002

servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)

try:
    servo.value = -0.5
    sleep(2)

    for i in range(5)
        servo.value = -1
        sleep(0.333)
        servo.value = -0.5
        sleep(0.333)

finally:
    GPIO.cleanup()