import socket
from time import sleep

port = 8833
host = '192.168.137.212'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print("Successfully connected to server")

for i in range(3):
    sleep(3)
    s.send(bytes(i))

s.send(bytes("end"))