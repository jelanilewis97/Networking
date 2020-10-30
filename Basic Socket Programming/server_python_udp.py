import socket
import time
import subprocess
import sys

IP = "127.0.0.1"
PORT = int(sys.argv[1])
BUFFER = 1500

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

while True:
	#set timeout to none so we can wait for first message from client
	sock.settimeout(None)
	data, addr = sock.recvfrom(BUFFER)
	sock.settimeout(0.5)
	#see if we receive command, if not wait for new client
	try:
		length = int.from_bytes(data, 'big')
		command, addr = sock.recvfrom(BUFFER)
		command = command.decode()
		if len(command) == length:
			sock.sendto('ACK'.encode(), addr)
	except socket.timeout:
		print("Failed to receive instructions from the client.")
		continue
	
	#run command and save result to file
	file = open('server.txt', 'w+')
	subprocess.run(command, shell=True, stdout=file)
	with open('server.txt', 'r') as file:
		data = file.read()

	#split data into chunks to be sent
	length = (len(data)).to_bytes(2, 'big')
	splitData = [data[i:i + 100] for i in range(0, len(data), 100)]
	sock.sendto(length, addr)

	#create loop that uses stop and wait reliability to send data
	numAttempts = 0
	arrayPosition = 0
	while True:
		if numAttempts > 3:
			print("File transmission failed.")
			break
		if arrayPosition >= len(splitData):
			break
		numAttempts += 1
		try:
			sock.sendto(splitData[arrayPosition].encode(), addr)
			ack, addr = sock.recvfrom(BUFFER)
			if ack.decode() != 'ACK':
				continue
			numAttempts = 0
			arrayPosition += 1
		except socket.timeout:
			continue


	file.close()
