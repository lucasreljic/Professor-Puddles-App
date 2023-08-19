import socket

port = 8833
host = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
