import socket
import time
import sys

BUFFER = 1500

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#take in ip, port, and command from user
serverIP = input("Enter server name or IP address:")
port = int(input("Enter port:"))
if int(port) < 0 or int(port) > 65535:
	print("Invalid port number")
	sys.exit()
command = input("Enter command:")
length = (len(command)).to_bytes(2, 'big')
sock.settimeout(1)
#attempt to send command/length to server, only continue when ack received
numTries = 0
while(True):
	try:
		sock.sendto(length, (serverIP, port))
		sock.sendto(command.encode(), (serverIP, port))
		data = sock.recv(BUFFER).decode()
		if data == 'ACK':
			break
	except socket.timeout:
		numTries += 1
		if numTries == 3:
			print("Failed to send command. Terminating.")
			sys.exit()
		continue
	else:
		print("Could not connect to server.")
		sys.exit()

#receive all packets of command's result
message = ''
data = sock.recv(BUFFER)
length = int.from_bytes(data, 'big')
numTries = 0
while(True):
	numTries += 1
	if len(message) == length:
		break
	try:
		data = sock.recv(BUFFER).decode()
		numTries = 0
		message += data
		sock.sendto('ACK'.encode(), (serverIP, port))
	except socket.timeout:
		if numTries > 3:
			print("Did not receive response.")
			sys.exit()
		continue

#once full message received save to file
f = open("client.txt", "w")
f.write(message)
f.close()
print("File saved")
