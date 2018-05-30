import time
import logging
import socket
import threading
import sys

window_size = 5
sended_packets = []
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(3)
addr = ("172.111.0.14", 1234)
listen = [0]

def server_send():
    for send_number in range(10000):
        send_number = str(send_number)

        while sended_packets and len(sended_packets) >= window_size:
            pass

        client_socket.sendto(send_number, addr)
        sended_packets.append([send_number, time.time()])

    listen.pop()

def listen_server():
    while listen or sended_packets:
        if not sended_packets:
            continue

        try:
            check_number, server = client_socket.recvfrom(1024)
            if check_number == sended_packets[0][0]:
                sended_packets[0][1] = False
                while sended_packets and sended_packets[0][1] is False:
                    sended_packets.pop(0)
            else:
                for bag in sended_packets:
                    if bag[0] == check_number:
                        bag[1] = False
                        break
        except socket.timeout:
            pass

        for bag in sended_packets:
            if bag[1] is not False and time.time() - bag[1] > 2:
                client_socket.sendto(bag[0], addr)
                bag[1] = time.time()



send_t  = threading.Thread(target=server_send)
send_t.start()
listen_t = threading.Thread(target=listen_server)
listen_t.start()

send_t.join()
listen_t.join()

print('All sent')
