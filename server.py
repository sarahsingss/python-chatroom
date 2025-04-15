import socket
import threading
import logging
from colorama import init, Fore, Style
from datetime import datetime

# Initialize the colorama import (colors for terminal messages/logs)
init(autoreset=True)

# ----------------------------------------------
# Server Settings:
# Sets up the server's host, port, and connection lists.
# ----------------------------------------------

HOST = '127.0.0.1'	# IP Address of the server
PORT = 55555		# Port number the server is listening on

# Logging settings 
logging.basicConfig(
	level=logging.INFO,
	format='[%(asctime)s] %(levelname)s - %(message)s',
	datefmt='%H:%M:%S'
)

clients = []      # Stores all connected client sockets
nicknames = []    # Stores nicknames (names) corresponding to each client


# ----------------------------------------------
# Utility Functions
# ----------------------------------------------

def format_server_message(message_text: str) -> bytes:
	"""
	Formats a message sent from the server.
	"""
	return f"Server: {message_text}".encode('utf-8')


def broadcast_message(message: bytes, sender_socket=None):
	"""
	Sends a message to all connected clients (excluding the sender).
	"""
	for client_socket in clients:
		if client_socket != sender_socket:
			try:
				client_socket.send(message)
			except Exception as e:
				logging.error(f"ERROR! Message was NOT sent: {e}")


# ----------------------------------------------
# Server Functions:
# Methods that handle client connections and message broadcasting
# ----------------------------------------------

def manage_client_session(client_socket: socket.socket):
	"""
	This function manages a single session: receives messages,
	broadcasts them to other clients, and handles disconnection.
	"""
	try:
		while True:
			message = client_socket.recv(1024)
			if message:
				broadcast_message(message, sender_socket=client_socket)

	except Exception as e:
		logging.warning(f"WARN! Client disconnected: {e}")

	finally:
		if client_socket in clients:
			index = clients.index(client_socket)
			nickname = nicknames[index]

			logging.info(f"{nickname} has disconnected. Users online: {len(clients) - 1}")
			clients.remove(client_socket)
			nicknames.remove(nickname)
			client_socket.close()
			broadcast_message(format_server_message(f"{nickname} has left the chat."))


def accept_client_connections():
	"""
	This function accepts new client connections, assigns nicknames to each connected 
	client, and starts a thread for each session.
	"""
	logging.info(f"Server is listening on {HOST}:{PORT}")

	while True:
		client_socket, address = server.accept()
		logging.info(f"New connection from {address}")

		# Request nickname
		client_socket.send(b'NICK')
		nickname = client_socket.recv(1024).decode('utf-8')

		# Handle duplicate nicknames
		if nickname in nicknames:
			client_socket.send(format_server_message("ERROR! This name is already taken. Please reconnect with a different name."))
			logging.warning(f"WARN! Rejected nickname: {nickname}")
			client_socket.close()
			continue

		# Store client information
		nicknames.append(nickname)
		clients.append(client_socket)

		logging.info(f"Name assigned: {nickname} | Users online: {len(clients)}")

		# Display welcome message
		broadcast_message(format_server_message(f"{nickname} joined the chat!"))
		client_socket.send(format_server_message("Welcome to the Chatroom! Type /quit to leave."))

		# Start thread for client session
		thread = threading.Thread(target=manage_client_session, args=(client_socket,))
		thread.start()


# ----------------------------------------------
# Main Function:
# This function handles the main loop of the server by
# starting the thread for accepting incoming client 
# connections.
# ----------------------------------------------

if __name__ == "__main__":
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((HOST, PORT))
		server.listen()
		accept_client_connections()

	except KeyboardInterrupt:
		logging.info("Shutting down server...")
		server.close()

	except Exception as e:
		logging.critical(f"WARN! Server failed to start: {e}")
