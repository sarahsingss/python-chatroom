import socket
import threading

# Ask the user for a nickname before connecting
nickname = input("Choose your nickname: ")

# Create a socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))  # Must match the server's host and port

# Function to receive messages from the server
def receive():
	while True:
		try:
			message = client.recv(1024).decode('utf-8')
			# If server requests nickname, send it
			if message == 'NICK':
				client.send(nickname.encode('utf-8'))
			else:
				# Print all other messages from server
				print(message)
		except:
			# In case of error (e.g. server down), exit
			print("An error occurred! Disconnecting from server.")
			client.close()
			break

# Function to send messages to the server
def write():
	while True:
		# Read input from user and send to server
		message = f'{nickname}: {input("")}'
		client.send(message.encode('utf-8'))

# Start receiving and writing in separate threads so they can run simultaneously
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

