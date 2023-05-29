import socket

IP = '192.168.1.40'
# home '192.168.0.102'

PORT = 5556
BUFF_SIZE = 65000


class ESP:
    def __init__(self):
        print('Подключение к микроконтроллеру')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((IP, PORT))
        sock.listen()
        self.conn, self.addr = sock.accept()
        print('Подключение успешно')

    def send_msg(self, msg):
        self.conn.send(str.encode(msg))