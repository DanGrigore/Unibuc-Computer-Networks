import random
import socket
import logging

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('172.111.0.14', 1234))

while True:
    message, address = server_socket.recvfrom(1024)
    print('%s - %s' % (message, address))
    server_socket.sendto(str(message), address)
