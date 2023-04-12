import pickle

import cv2, imutils, socket
import numpy as np
import time
import base64
from face_recognizer import FaceRecognizer

BUFF_SIZE = 65000
IP = "127.0.0.1"
PORT = 5000
fps,st,frames_to_count,cnt = (0,0,20,0)

sfr = FaceRecognizer()
sfr.load_encodings_from_database()

def fun_feature(image):
    import face_recognition
    face_landmarks_list = face_recognition.face_landmarks(image)
    if bool(face_landmarks_list):
        for point_list in face_landmarks_list[0].values():
            for point in point_list:
                image = cv2.circle(image, point, 2, (255,255,255), 2)
    return


def face_rec(fr):
    '''Рисует квадратики с лицами, msg - если кто-то знакомый, то True'''
    locations, names = sfr.detect_known_faces(fr)
    msg = "0"
    for location, name in zip(locations, names):
        cv2.rectangle(fr, (location[1], location[0]), (location[3], location[2]), (250, 0, 0), 2)
        cv2.putText(fr, name, (location[1] - 10, location[0]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        msg = "Открывай дверь, там {} пришел(а)".format(name)
    return msg

if __name__ == '__main__':
    print('hi im server')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen()
    conn, addr = sock.accept()
    while True:
        msg, address = conn.recvfrom(BUFF_SIZE)

        WIDTH = 640
        imageDict = pickle.loads(msg)
        names = sfr.identify(imageDict['encodings'])

        conn.send(str.encode('Открывай, там {} пришел(а)'.format(names)))









