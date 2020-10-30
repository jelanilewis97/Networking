import socket
import sys
import time

BUFFER = 1500

#take in input, port, and command from user
serverIP = input("Enter server name or IP address:")
port = int(input("Enter port:"))
if port < 0 or int(port) > 65535:
	print("Invalid port number")
	sys.exit()
command = input("Enter command:")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
#try connecting to server
try:
	s.connect((serverIP, port))
except (ConnectionRefusedError, socket.timeout):
	print("Could not connect to server.")
	sys.exit()

#send command to server
s.send(command.encode())
data = s.recv(BUFFER)
s.close()

#save command output to file
f = open("client.txt", "w")
f.write(data.decode())
f.close()
print("File saved")