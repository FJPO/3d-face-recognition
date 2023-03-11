import pickle

import cv2, imutils, socket
import numpy as np
import time
import base64
from realsense_camera import RealsenseCamera

CAMERA_USE_PARAM = 1 #'В аргументы команндной строли введите 0 для веб камеры или 1 для камеры realsense'

UDP_IP = "127.0.0.1"
SERVER = 5000

buffer_size = 65536

fps,st,frames_to_count,cnt = (0,0,20,0)


cam, vid = None, None
def getCurrentFrame():
    d = []
    if cam != None:
        _, frame, d = cam.get_frame_stream()
    else:
        _, frame = vid.read()
    return frame, d

def encode_image(img, depth):
    # encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    #
    # message = base64.b64encode(buffer)
    # return message
    msg = {'rgb': img, 'd': depth}

    return pickle.dumps(msg)

if __name__ == '__main__':
    if CAMERA_USE_PARAM == 1:
        cam = RealsenseCamera()
        vid = cam.get_frame_stream()
        print('Запись видео с realsense')
    else:
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print('Запись видео с web камеры')
    time.sleep(4)
    print('hi im client')
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind((UDP_IP, 0))
    while True:
        WIDTH = 100 #640
        # while (vid.isOpened()):
        while True:
            frame, d = getCurrentFrame()

            depth_frame = np.array(d)
            depth_frame[depth_frame > 3000] = 3000
            depth_frame = depth_frame / 3000
            cv2.imshow("DEPTH VIDEO original", depth_frame)


            frame = imutils.resize(frame, width=WIDTH)
            if CAMERA_USE_PARAM == 1:
                d = imutils.resize(d, width=WIDTH)

            message = encode_image(frame, d)

            socket.sendto(message, (UDP_IP, SERVER))
            msg, _ = socket.recvfrom(buffer_size)
            msg = msg.decode()
            if msg != '0': print(msg)
            # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.imshow('TRANSMITTING VIDEO', frame)
            d
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1
