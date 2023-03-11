import pickle

import cv2, imutils, socket
import numpy as np
import time
import base64
from face_recognizer import FaceRecognizer

BUFF_SIZE = 65536
UDP_IP = "127.0.0.1"
UDP_PORT = 5000
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        msg, address = sock.recvfrom(BUFF_SIZE)

        WIDTH = 400
        imageDict = pickle.loads(msg)
        frame = imageDict['rgb']
        frame = imutils.resize(frame, width=WIDTH)
        depth_frame = imageDict['d']
        depth_frame = imutils.resize(depth_frame, width=WIDTH)


        # data = base64.b64decode(msg, ' /')
        # npdata = np.frombuffer(data, dtype=np.uint8)
        #
        # frame = cv2.imdecode(npdata, 1)

        # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        sock.sendto(str.encode(face_rec(frame)), address)
        # fun_feature(frame)
        cv2.imshow("RECEIVING VIDEO", frame)
        depth_frame = np.array(depth_frame)
        depth_frame[ depth_frame > 3000 ] = 3000
        depth_frame = depth_frame / 3000
        cv2.imshow("DEPTH VIDEO", depth_frame)



        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            sock.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1








