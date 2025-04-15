# Chatroom Application

## Project Overview

This is a basic **client-server socket application** implemented in **Python**, which allows multiple users to communciate through messages in real-time over a local network.

The server manages connections and broadcasts messages to all connected clients, while each client connects via a simple terminal interface.

## How to run
- run "pip install colorama"
- make sure to have python installed
- run server first using "python server.py"
- next run client, using "python client.py"


## Features

- Real-time multi-user communication using sockets
- Concurrent client handling using Python's `threading` module
- User nickname registration and message broadcasting
- Does not require any third-party dependencies


## How it works

1. **Server**:  
    - Accepts and manages incoming client connections  
    - Prompts each client for a unique nickname upon joining  
    - Handles message broadcasting to all connected clients  
    - Detects and cleans up disconnected clients

2. **Client**:  
    - Establishes a connection to the server using a defined nickname  
    - Utilizes multithreading to send and receive messages simultaneously  
    - Users interact with the application via a simple command-line interface 


## Software Framewok

- **Language**: Python
- **Socket Library**: Built-in `socket` package
- **Concurrency**: Built-in `threading` package
- **IDE**: Visual Studio Code
- **Version Control**: Git + GitHub


## Team Members and Roles

| Name                  | Role                                      |
|-----------------------|-------------------------------------------|
| Aidan Potter          | Server-side Development                   |
| Quinn Hankes          | Client-side Development                   |
| Sarah Singhirunnusorn | Project Documentation                     |

---
