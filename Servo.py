from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)

#servo pins
minPW=0.001
maxPW=0.002

try:
    servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)
    servo.vaue = 0.5
    

finally:
    GPIO.cleanup()