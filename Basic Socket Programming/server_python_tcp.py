import socket
import os
import subprocess
import sys

IP = '127.0.0.1'
PORT = int(sys.argv[1])
BUFFER = 1500

#bind socket to designated ip and port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)

#accept connection from client
conn, addr = s.accept()
file = open('server.txt', 'w+')
while True:
	#take received data, save to file, read to file, and then send back to client
    data = conn.recv(BUFFER).decode()
    if not data: 
    	break
    subprocess.run(data, shell=True, stdout=file)
    with open('server.txt', 'r') as file:
    	data = file.read()
    conn.send(data.encode())
    
file.close()
conn.close()