from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
import pygame

GPIO.setmode(GPIO.BCM)

#servo pins
minPW=0.0004
maxPW=0.004

servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)
servo2 = AngularServo(14,min_pulse_width=minPW,max_pulse_width=maxPW)

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def Water():
    default = -0.5
    delay = 0.333
    servo.value = default
    servo2.value = default
    sleep(2)

    play_mp3("Quack.mp3")

    for i in range(5):
        servo.value = -1
        servo2.value = -1
        sleep(delay)
        servo.value = default
        servo2.value = default
        sleep(delay)
    

try:
    Water()

finally:
    print("-------------------------")
    GPIO.cleanup()