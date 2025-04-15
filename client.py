import socket
import threading
import logging
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize the colorama import (colors for terminal messages/logs)
init(autoreset=True)

# ----------------------------------------------
# Client Settings:
# Defines how the client connects to the server
# ----------------------------------------------

HOST = '127.0.0.1'	# IP Address of the server
PORT = 55555		# Port number the server is listening on

# Logging settings 
logging.basicConfig(
	level=logging.INFO,
	format='[%(asctime)s] %(levelname)s - %(message)s',
	datefmt='%H:%M:%S'
)


# ----------------------------------------------
# Client Functions:
# Methods that handle how the client sends and receives messages
# ----------------------------------------------

def format_chat_message(sender_name, message_text, from_self=False, from_system=False):
	"""
	This function formats how messages are displayed in the chat.
	"""
	timestamp = datetime.now().strftime('%H:%M')
	if from_system:
		return f"{Fore.LIGHTMAGENTA_EX}[{timestamp}] [Server]: {message_text}{Style.RESET_ALL}"
	elif from_self:
		return f"{Fore.GREEN}[{timestamp}] [You]: {message_text}{Style.RESET_ALL}"
	else:
		return f"{Fore.CYAN}[{timestamp}] [{sender_name}]: {message_text}{Style.RESET_ALL}"


def receive_chat_messages(client_socket: socket.socket):
	"""
	This function handles how the client interprets and displays incoming 
	messages from the server.
	"""
	try:
		while True:
			# Receive and decode the message from the server
			incoming_message = client_socket.recv(1024).decode('utf-8')
			if not incoming_message:
				logging.warning("Connection CLOSED -> Disconnected from server.")
				break
			
			# Server requests client's nickname for identification
			if incoming_message == 'NICK':
				client_socket.send(nickname.encode('utf-8'))
				continue 
			
			# Print received messages based on their message type
			if incoming_message.startswith(f"{nickname}:"):
				print_self_message(incoming_message)
			elif incoming_message.startswith("Server:"):
				print_system_message(incoming_message)
			else:
				print_received_message(incoming_message)

	except Exception as e:
		logging.error(f"ERROR! Message NOT received: {e}")
	finally:
		logging.warning("Closing connection...")
		client_socket.close()
		sys.exit()


def send_chat_messages(client_socket: socket.socket):
	"""
	This function handles how the client sends messages to the server.
	"""
	try:
		while True:
			# Prompt user to enter a message
			prompt = f"{Fore.LIGHTBLACK_EX}{nickname} ✉️  > {Style.RESET_ALL}"
			message_text = input(prompt)

			# Handles user input for leaving the chat ("/quit" command)
			if message_text.strip().lower() == "/quit":
				logging.info("Disconnecting from server...")
				client_socket.send(f"Server: {nickname} has left the chat.".encode('utf-8'))
				client_socket.close()
				print(Fore.YELLOW + "You have left the chat." + Style.RESET_ALL)
				sys.exit()

			# Format and send message to server
			formatted_message = f"{nickname}: {message_text}"
			client_socket.send(formatted_message.encode('utf-8'))

	except Exception as e:
		logging.error(f"ERROR! Message NOT sent: {e}")
		client_socket.close()
		sys.exit()


# ----------------------------------------------
# Utility Functions:
# ----------------------------------------------

def print_self_message(incoming_message: str):
	"""
	Prints the message sent by the client/user.
	"""
	message_text = incoming_message[len(nickname) + 2:]
	print(format_chat_message(nickname, message_text, from_self=True))

def print_system_message(incoming_message: str):
	"""
	Prints system message (messages from the server) (ex: user joined).
	"""
	message_text = incoming_message[len("Server: "):]
	print(format_chat_message("Server", message_text, from_system=True))

def print_received_message(incoming_message: str):
	"""
	Prints messages received from other clients/users.
	"""
	try:
		sender_name, message_text = incoming_message.split(":", 1)
		print(format_chat_message(sender_name.strip(), message_text.strip()))
	except ValueError:
		logging.warning(f"Invalid message format: {incoming_message}")


# ----------------------------------------------
# Main Function:
# This function handles the main loop of the client by
# starting the thread for sending and receiving messages 
# to/from the server
# ----------------------------------------------
if __name__ == "__main__":
	try:
		while True:
			# Prompt the user for a valid name
			nickname = input("Enter your name: ").strip()
			if nickname:
				break
			print("Name cannot be EMPTY! Please enter a valid name.")
		
		# Create socket and connect to the server
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((HOST, PORT))
		logging.info(f"Connected to server at {HOST}:{PORT}")
		
		# Show welcome message
		print(Fore.CYAN + "\nWelcome to the Chatroom! Type your message and press Enter to send." + Style.RESET_ALL)
		print(Fore.LIGHTBLACK_EX + "Type /quit to leave at any time!\n" + Style.RESET_ALL)
		
		# Begin message thread
		receive_thread = threading.Thread(target=receive_chat_messages, args=(client_socket,))
		send_thread = threading.Thread(target=send_chat_messages, args=(client_socket,))

		receive_thread.start()
		send_thread.start()

		# Keep main thread alive until both finish
		receive_thread.join()
		send_thread.join()
	
	except KeyboardInterrupt:
		logging.info("Exited chatroom via keyboard interrupt.")
		client_socket.close()
		sys.exit()

	except Exception as e:
		logging.critical(f"Connection FAILED: {e}")
		sys.exit(1)



