# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 12:59:07 2019

@author: Happy Ta
"""

import socket
import select

# setup
HEADER_LENGTH = 10
IP = ''
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reuse same port to avoid port already occupied
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))      # Bind IP and PORT and get socket ready to receive requests
server_socket.listen()              # server start listening for TCP request

sockets_list = [server_socket]

clients = {}

print(f'Listening for connections...')


# Handles message receiving
# noinspection PyBroadException
def receive_message(client_socket):

    try:

        # Grab header
        message_header = client_socket.recv(HEADER_LENGTH)

        # If there aren't any data, a client closed the connection
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print("Accepted new connection from {}:{}, username: {}".format(*client_address, user["data"].decode("utf-8")))

        else:
            message = receive_message(notified_socket)

            if message is False:
                print("Closed connection from: {}".format(clients[notified_socket]["data"].decode("utf-8")))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            # Send message to every connected clients
            for client_socket in clients:
                # But does not send it to the original sender
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # handle any exception
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
