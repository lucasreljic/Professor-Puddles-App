import socket

port = 8833
host = '192.168.137.212' #socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print("Successfully connected to server")