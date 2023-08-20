from argparse import Action
from http import client
import socket
from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#socket params
port = 8833
host = '192.168.137.212' 

#servo pins
minPW=0.0004
maxPW=0.004

servo = AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)
default = -0.5
delay = 0.333
servo.value = default

def Water():
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
            #if v == "1":
            #    Action1()
            #if v == "2":
            #    Action2()
            #v represents which servo
            v = clientsocket.recv(8).decode('utf-8')

        print("Client disconnected")

finally:
    GPIO.cleanup()