# {{ host.name }}: main.py: {{ host.description }}

import time
import usocket as socket

import hosts

def sendudp(host, port, *data):
    address = (hosts.by_name['bob'], port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for d in data:
        sock.sendto(d, address)

p_count = 0
while True:
    time.sleep(2)
    p_count += 1
    sendudp('bob', 6969, b'Packet number %s {{ host.name }}' % p_count)
