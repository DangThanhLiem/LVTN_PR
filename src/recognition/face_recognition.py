import face_recognition
import cv2
import numpy as np
from typing import List, Tuple

class FaceRecognitionSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []

    def add_face(self, image_path: str, employee_id: str, name: str):
        """
        Thêm gương mặt vào hệ thống nhận diện.
        
        :param image_path: Đường dẫn đến hình ảnh của gương mặt.
        :param employee_id: ID của nhân viên.
        :param name: Tên của nhân viên.
        """
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)
        self.known_face_ids.append(employee_id)

    def recognize_face(self, frame: np.ndarray) -> Tuple[List[Tuple[int, int, int, int]], List[str], List[str]]:
        """
        Nhận diện gương mặt trong khung hình.

        :param frame: Khung hình chứa gương mặt cần nhận diện.
        :return: Danh sách vị trí gương mặt, tên và ID của nhân viên.
        """
        # Resize frame for faster face recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        face_ids = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            employee_id = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                employee_id = self.known_face_ids[first_match_index]
            face_names.append(name)
            face_ids.append(employee_id)

        # Convert face locations back to original frame size
        face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]

        return face_locations, face_names, face_ids
