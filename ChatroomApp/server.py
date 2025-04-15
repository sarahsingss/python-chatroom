import socket
import threading

# Define the IP address and port for the server to listen on
HOST = '127.0.0.1'  # Localhost (only accessible on the same machine)
PORT = 55555        # Arbitrary non-privileged port

# Create a socket object and bind it to the host and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lists to keep track of connected clients and their nicknames
clients = []
nicknames = []

# Broadcast a message to all connected clients
def broadcast(message):
	for client in clients:
		client.send(message)

# Handle communication with a single client
def handle(client):
	while True:
		try:
			# Receive messages from this client
			message = client.recv(1024)
			# Broadcast the received message to everyone
			broadcast(message)
		except:
			# If error (client disconnected), remove them
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			# Let everyone know the user left
			broadcast(f'{nickname} left the chat!'.encode('utf-8'))
			nicknames.remove(nickname)
			break

# Accept new clients and assign them nicknames
def receive():
	print(f"Server running on {HOST}:{PORT}...")
	while True:
		client, address = server.accept()
		print(f"Connected with {str(address)}")

		# Ask for nickname
		client.send('NICK'.encode('utf-8'))
		nickname = client.recv(1024).decode('utf-8')
		nicknames.append(nickname)
		clients.append(client)

		# Announce new client
		print(f"Nickname is {nickname}")
		broadcast(f"{nickname} joined the chat!".encode('utf-8'))
		client.send('Connected to the server!'.encode('utf-8'))

		# Start a new thread to handle this client
		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

# Start the server
receive()

