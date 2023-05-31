# echo-client.py 
import socket
# The server's hostname or IP address
HOST = "127.0.0.1"
# The port used by the server
PORT = 7000

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"Hello, world!")
    data = s.recv(1024)
    
print(f"received {data!r}")