# firstboot.py - this file produced automatically - edits may be reverted

from network import WLAN, STA_IF, AP_IF

sta_if, ap_if = WLAN(STA_IF), WLAN(AP_IF)
ap_if.active(False)
sta_if.active(True)
if not sta_if.isconnected():
    print('connecting to network {{ net.ssid }}...')
    sta_if.connect('{{ net.ssid }}', '{{ net.password }}')
    while not sta_if.isconnected():
        pass
    sta_if.ifconfig(['{{ host.ip_address}}', '{{ net.mask }}', '{{ net.gateway }}', '{{ net.dns_server }}'])
    print("Connected")


import usocket

def load_file(file_name):
    print(file_name)
    data = []
    sock = usocket.socket()
    sock.connect(('{{ net.boot_server }}', 8000))
    sock.send(b'GET /%s HTTP/1.0\r\n\r\n' % (file_name, ))
    with open(file_name, 'w') as outf:
        while True:
            new_data = sock.read(1024)
            if not new_data:
                break
            data.append(new_data)
        data = b''.join(data)
        # It might be a good idea to check the server status code here ...
        pos = data.find(b'\r\n\r\n')+4
        n = outf.write(data[pos:])

for file_name in {{ host.files }}:
    load_file(file_name)
