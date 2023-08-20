from argparse import Action
from http import client
import socket
from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
import pygame

GPIO.setmode(GPIO.BCM)

#socket params
port = 8833
host = '192.168.137.139' 

#servo pins
minPW=0.0004
maxPW=0.004

servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)
default = -0.5
delay = 0.333
servo.value = default
pygame.mixer.init()

def play_mp3(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def Water():
    play_mp3("Quack.mp3")
    for i in range(5):
        servo.value = -1
        sleep(delay)
        servo.value = default
        sleep(delay)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("Socket initialized")
print(host)

try:
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")

        v = clientsocket.recv(8).decode('utf-8')
        while v != "end":
            if v == "0":
                print("Recieved 0")
                play_mp3("Quack.mp3")
            if v == "1":
                print("Recieved 1")
                play_mp3("Stop.mp3")
            if v == "2":
                print("Recieved 2")
                play_mp3("Final.mp3")
            if v == "3":
                print("Recieved 3")
            if v == "4":
                print("Recieved 4")
                Water()
            v = clientsocket.recv(8).decode('utf-8')

        print("Client disconnected")

finally:
    GPIO.cleanup()