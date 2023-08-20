from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
from playsound import playsound

GPIO.setmode(GPIO.BCM)

#servo pins
minPW=0.0004
maxPW=0.004

servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)

def Water():
    default = -0.5
    delay = 0.333
    servo.value = default
    sleep(2)

    playsound('Quack.mp3')

    for i in range(5):
        servo.value = -1
        sleep(delay)
        servo.value = default
        sleep(delay)
    

try:
    Water()

finally:
    GPIO.cleanup()