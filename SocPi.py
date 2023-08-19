from argparse import Action
from http import client
import socket

port = 8833
host = '192.168.137.212' 

def Action1():
    print("1")

def Action2():
    print("2")

def Action3():
    print("3")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("Socket initialized")
print(host)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    v = clientsocket.recv(8)
    while v != "end":

        v = clientsocket.recv(8)
        if v == "1":
            Action1()
        if v == "2":
            Action2()
        if v == "3":
            Action3()

    print("Client disconnected")


