# -*- coding: utf-8 -*-
"""
Created on Sat Nov  14 13:18:00 2019

@author: Happy Ta
"""

import socket
import select
import errno
import sys

# setup
IP = input('Enter Server IP: ')


HEADER_LENGTH = 10

PORT = 1234
my_userName = input('Username: ')  # Retrieve user's name


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create a socket
client_socket.connect((IP, PORT))                                       # Connect to server's IP and Port
client_socket.setblocking(False)                                        # setblocking is false so .recv() wont block, it'll just return exception which can be handle

username = my_userName.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while message.lower().strip() != 'exit':
    message = input(f"{my_userName} > ")  #TODO fix

    # if message is not empty => send it
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Loop to print recieved message
        while True:
            userName_header = client_socket.recv(HEADER_LENGTH)
            if not len(userName_header):  # check length of header if = 0 => connection closed => close the program
                print('Connection closed by server')
                sys.exit()

            # grab username header and username data from server of other users
            userName_length = int(userName_header.decode('utf-8').strip())
            userName = client_socket.recv(userName_length).decode('utf-8')

            # grab message header and message data from server of other users
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{userName} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Normal error: '.format(str(e)))
        sys.exit()
