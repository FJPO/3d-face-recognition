import pickle

import face_recognition
import cv2, imutils, socket
import numpy as np
import time
from esp_module import ESP
from realsense_camera import RealsenseCamera

CAMERA_USE_PARAM = 1 #'В аргументы команндной строли введите 0 для веб камеры или 1 для камеры realsense'
tempo = False
IP = "127.0.0.1"
SERVER = 5000

buffer_size = 65000

fps,st,frames_to_count,cnt = (0,0,20,0)
FRAME_RESIZE_FOR_RECOGNITION = 0.25

cam, vid = None, None
def getCurrentFrame():
    d = []
    if cam != None:
        _, frame, d = cam.get_frame_stream()
    else:
        _, frame = vid.read()
    return frame, d

def encode_image(img, depth):
    small_frame = cv2.resize(img, (0, 0), fx=FRAME_RESIZE_FOR_RECOGNITION, fy=FRAME_RESIZE_FOR_RECOGNITION)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    msg = {'encodings': face_encodings}
    for location in np.array(face_locations) / FRAME_RESIZE_FOR_RECOGNITION:
        location = location.astype(int)
        cv2.rectangle(frame, (location[1], location[0]), (location[3], location[2]), (250, 0, 0), 2)
        # cv2.imwrite('test.jpg', depth)
    cv2.imshow('TRANSMITTING VIDEO', img)


    # maxx = 800
    # for i in range(depth.shape[0]):
    #     for j in range(depth.shape[1]):
    #         if depth[i][j] >= maxx:
    #             depth[i][j] = maxx
    #         depth[i][j] = int(depth[i][j]/maxx*255)



    # colorizer = rs.colorizer(color_scheme=3)
    # depth_colormap = np.asanyarray(colorizer.colorize(depth).get_data())
    # cv2.imwrite('test.jpg', cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR))
    # print(cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR).shape, cv2.cvtColor(depth, cv2.COLOR_GRAY2BGR))
    return len(face_encodings) != 0, pickle.dumps(msg)

if __name__ == '__main__':
    est = ESP()
    if CAMERA_USE_PARAM == 1:
        cam = RealsenseCamera()
        vid = cam.get_frame_stream()
        print('Запись видео с камеры realsense')
    else:
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print('Запись видео с web камеры')
    time.sleep(4)
    print('Клиент начал работу.')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, SERVER))
    while True:
        WIDTH = 640
        while True:
            frame, d = getCurrentFrame()
            frame = imutils.resize(frame, width=WIDTH)
            if CAMERA_USE_PARAM == 1:
                d = imutils.resize(d, width=WIDTH)
            isAny, message = encode_image(frame, d)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                sock.close()
                quit(0)
            if isAny:
                sock.send(message)
                msg, _ = sock.recvfrom(buffer_size)
                msg = msg.decode()
                # if not tempo:
                print(msg)
                tempo = True
                est.send_msg(msg)


