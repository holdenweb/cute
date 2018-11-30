# {{ host.name }}: main.py: {{ host.description }}

import time
import usocket as socket

import hosts

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('{{ host.ip_address }}', 6969))
print("Starting rececive loop")

while True:
    data, address = sock.recvfrom(1000)
    print(data.decode('utf-8'))
