from side.side_gui import side_gui
from front.front_gui import front_gui
import socket
from time import sleep

port = 8383
host = '192.168.137.139'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = True
try:
    s.connect((host, port))
except:
    print("could not connect to duck :(")
    connect = False
    s = None
if connect:
    print("Successfully connected to duck!")
if __name__ == "__main__":
    front_gui(s)
    print("disconnecting...")
    try:
        s.send(bytes("end".encode('utf-8')))
    except:
        print("Done!")