from argparse import Action
from http import client
import socket
from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)

#socket params
port = 8833
host = '192.168.137.212' 

#servo pins
servos = [14, 15, 18]

def Action0():
    print("0")

def Action1():
    print("1")

def Action2():
    print("2")

def ServoInitialize():
    for v in servos:
        servo = Servo(v)
        servo.value = 0

def ServoTester(pin):
    print(pin)
    servo = Servo(pin)
    servo.value = 1
    sleep(1)
    servo.value = 0

try:

    ServoInitialize()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("Socket initialized")
    print(host)

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
            try:
                n = int(v)
                print(n)
            except:
                print("Non int recieved")
            ServoTester[int(v)]
            v = clientsocket.recv(8).decode('utf-8')

        print("Client disconnected")

finally:
    GPIO.cleanup()
