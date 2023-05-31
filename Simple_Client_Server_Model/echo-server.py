# echo-server.py
import socket
# Standard loopback interface address (localhost)
HOST = "127.0.0.1" 
# Port to listen on (non-privileged ports are >1023)
PORT = 7000
# Create a socket object that support the context manager type, so you can use it in a with statement. 
# There's no need to call s.close()

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
# Use the socket object without calling s.close().
    s.bind((HOST, PORT))
# The .bind() method is used to associate the socket with a specific network interface and port number.
    s.listen()
# The .listen() enbales a server to acceept connections. 
# The .listen() methods has a backlog parameter.
    conn,addr = s.accept()
# The .accept() method blocks execution and waits for an incoming connection.
    with conn: 
        print(f"Connected by {addr}")
        while True:
# An infinite while LOOP is used to over blocking calls to conn.recv().
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
# This reads whatever data the client sends and echoes it back using conn.sendall().
# If conn.recv() returns an empty bytes object, b'', that signals that the client closed the connection and the loop is terminated.
# The with STATEMENT is used with conn to automatically close the socket at the end of the block.


    
