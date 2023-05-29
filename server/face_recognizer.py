import face_recognition
import cv2
import os
import glob
import numpy as np

class FaceRecognizer:
    known_face_encodings = []
    known_face_names = []
    frame_resizing = 0.25

    @staticmethod
    def load_encoding_images_from_file(images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            FaceRecognizer.known_face_encodings.append(img_encoding)
            FaceRecognizer.known_face_names.append(filename)
        print("Encoding images loaded")

    @staticmethod
    def load_encodings_from_database():
        from db_interactor import DB_interactor
        for t in DB_interactor.load_all():
            FaceRecognizer.known_face_names.append(t[0])
            FaceRecognizer.known_face_encodings.append(t[1])

    @staticmethod
    def identify(face_encodings):
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(FaceRecognizer.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was founFaceRecognizer.known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     FaceRecognizer.known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(FaceRecognizer.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = FaceRecognizer.known_face_names[best_match_index]
            face_names.append(name)
        return face_names


    @staticmethod
    def detect_known_faces(frame):
        small_frame = cv2.resize(frame, (0, 0), fx=FaceRecognizer.frame_resizing, fy=FaceRecognizer.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)



        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / FaceRecognizer.frame_resizing
        return face_locations.astype(int), FaceRecognizer.identify(face_encodings)

    @staticmethod
    def get_vector(path):
        img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        vector = face_recognition.face_encodings(img)[0]
        return vector




