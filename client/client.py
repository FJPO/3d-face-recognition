import pickle

import face_recognition
import cv2, imutils, socket
import numpy as np
import matplotlib.pyplot as plt
import time
import PIL.Image as im
import base64
from realsense_camera import RealsenseCamera

CAMERA_USE_PARAM = 1 #'В аргументы команндной строли введите 0 для веб камеры или 1 для камеры realsense'

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
    depth = np.array(depth)
    depth[depth > 3000] = 3000
    depth = (depth) / 3000 * 255
    depth = cv2.cvtColor(depth.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    img = depth
    cv2.imwrite('../server/face_data/ilya-deep.jpg', depth)
    quit(0)
    small_frame = cv2.resize(img, (0, 0), fx=FRAME_RESIZE_FOR_RECOGNITION, fy=FRAME_RESIZE_FOR_RECOGNITION)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # try grayscale conversion
    # rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_RGB2GRAY)
    # # rgb_small_frame = np.reshape(rgb_small_frame, np.append(np.array(rgb_small_frame.shape), 1))
    # rgb_small_frame_new = np.zeros(np.append(np.array(rgb_small_frame.shape), 3))
    # for i in range(rgb_small_frame.shape[0]):
    #     for j in range(rgb_small_frame.shape[1]):
    #         rgb_small_frame_new[i, j] = [rgb_small_frame[i][j], rgb_small_frame[i][j], rgb_small_frame[i][j]]
    # rgb_small_frame = rgb_small_frame_new.astype(int)
    # print(rgb_small_frame.shape)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    msg = {'encodings': face_encodings}

    for location in np.array(face_locations) / FRAME_RESIZE_FOR_RECOGNITION:
        location = location.astype(int)
        cv2.rectangle(frame, (location[1], location[0]), (location[3], location[2]), (250, 0, 0), 2)
    cv2.imshow('TRANSMITTING VIDEO', frame)


    return len(face_encodings) != 0, pickle.dumps(msg)

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, SERVER))
    while True:
        WIDTH = 640 #640
        # while (vid.isOpened()):
        while True:
            frame, d = getCurrentFrame()


            depth_frame = np.array(d)
            depth_frame[depth_frame > 3000] = 3000
            depth_frame = (depth_frame)/3000

            depth_frame.astype(np.uint8)
            # cv2.imshow("DEPTH VIDEO original", depth_frame)
            colormap = plt.get_cmap('inferno')
            heatmap = (colormap(depth_frame) * 2 ** 15).astype(np.uint16)[:, :, :3]
            heatmap = cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR)
            cv2.imshow("DEPTH VIDEO original", heatmap)



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
                print(msg)



