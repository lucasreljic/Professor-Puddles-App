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
minPW=0.001
maxPW=0.002

servos = [AngularServo(14,min_pulse_width=minPW,max_pulse_width=maxPW), 
          AngularServo(15,min_pulse_width=minPW,max_pulse_width=maxPW),
         AngularServo(18,min_pulse_width=minPW,max_pulse_width=maxPW)]

def Action0():
    print("0")

def Action1():
    print("1")

def Action2():
    print("2")

def ServoInitialize():
    for servo in servos:
        servo.value = 0

def ServoTester(i):
    print(i)
    servo = servos[i]
    servo.value = 1
    sleep(1)
    servo.value = -1


ServoInitialize()
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
            #if v == "0":
            #    Action0()
            #if v == "1":
            #    Action1()
            #if v == "2":
            #    Action2()
            ServoTester(int(v)) #v represents which servo
            v = clientsocket.recv(8).decode('utf-8')

        print("Client disconnected")

finally:
    GPIO.cleanup()