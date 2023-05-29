import pickle
from datetime import datetime

import socket
from face_recognizer import FaceRecognizer

BUFF_SIZE = 65000
IP = "127.0.0.1"
logfile = 'server.log'
PORT = 5000

fr = FaceRecognizer()
fr.load_encodings_from_database()

if __name__ == '__main__':
    print('Сервер работает')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen()
    conn, addr = sock.accept()
    while True:
        msg, address = conn.recvfrom(BUFF_SIZE)

        WIDTH = 640
        imageDict = pickle.loads(msg)
        names = fr.identify(imageDict['encodings'])
        resp = 'Обнаружен пользователь: {}'.format(names)
        if names[0] == 'Unknown':
            resp = 'Обнаружен пользователь: {}, доступ не предоставлять'.format(names)
        else:
            resp = 'Обнаружен пользователь: {}, предоставить доступ'.format(names)
        conn.send(str.encode(resp))
        with open(logfile, 'a') as f:
            f.write('{} {}\n'.format(datetime.now(),resp))