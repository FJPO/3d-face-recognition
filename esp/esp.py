import machine
import time
import network
import socket

#IP = '192.168.0.102'
IP = '192.168.1.40'
SERVER = 5556
buffer_size = 1024
wifi_name = 'TP-Link_9AAC'
wifi_pwd = ''

def do_connect():
    time.sleep(0.1)
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        print (f'started in the connected state, but now disconnected')
    else:
        print (f'started in the disconnected state')
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ichiro-home-1')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

p = machine.Pin(18, machine.Pin.OUT)



do_connect()
print('подключение сокета')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, SERVER))

print('сокет подключен')
while True:
    msg, _ = sock.recvfrom(buffer_size)
    msg = msg.decode()
    print(msg)
    if (msg.endswith('предоставить доступ')):
        p.on()
        time.sleep(5)
        p.off()

