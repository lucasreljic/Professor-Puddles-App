import socket

port = 8833
host = '192.168.137.212' #socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("Socket initialized")
print(host)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")


