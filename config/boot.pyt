# boot.py - this file produced automatically - edits may be reverted

from network import WLAN, STA_IF

sta_if = WLAN(STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
    print('connecting to network {{ net.name }}...')
    sta_if.connect('{{ net.name }}', '{{ net.password}}')
    while not sta_if.isconnected():
        pass
    sta_if.ifconfig(['{{ host.ip_address }}', '{{ net.mask }}', '{{ net.gateway }}', '{{ net.dns_server }}'])
    print("Connected")
