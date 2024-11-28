from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from datetime import datetime
from src.recognition.face_recognition import FaceRecognitionSystem

class AttendanceTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.face_recognition = FaceRecognitionSystem()
        self.init_ui()
        self.load_known_faces()

    def init_ui(self):
        layout = QVBoxLayout()

        # Camera preview
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(640, 480)
        layout.addWidget(self.camera_label)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Camera")
        self.stop_btn = QPushButton("Stop Camera")
        self.check_in_btn = QPushButton("Check In")
        self.check_out_btn = QPushButton("Check Out")

        self.start_btn.clicked.connect(self.start_camera)
        self.stop_btn.clicked.connect(self.stop_camera)
        self.check_in_btn.clicked.connect(self.check_in)
        self.check_out_btn.clicked.connect(self.check_out)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.check_in_btn)
        btn_layout.addWidget(self.check_out_btn)
        layout.addLayout(btn_layout)

        # Attendance table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Employee ID", "Name", "Date", "Check In", "Check Out", "Total Hours"])
        layout.addWidget(self.table)

        # Export button
        export_btn = QPushButton("Export Report")
        export_btn.clicked.connect(self.export_report)
        layout.addWidget(export_btn)

        self.setLayout(layout)
        
        # Camera timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None

    def load_known_faces(self):
        # Load employee faces from database
        employees = self.db.collection('Employee').get()
        for employee in employees:
            data = employee.to_dict()
            image_path = f'data/employee_images/{data["id"]}.jpg'
            try:
                self.face_recognition.add_face(image_path, data['id'], data['name'])
            except Exception as e:
                print(f"Error loading face for employee {data['id']}: {str(e)}")

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
        self.camera_label.clear()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Recognize faces
            face_locations, face_names, face_ids = self.face_recognition.recognize_face(frame)

            # Draw rectangles around faces
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Convert to Qt format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qt_image))

    def check_in(self):
        # Implement check-in logic
        pass

    def check_out(self):
        # Implement check-out logic
        pass

    def export_report(self):
        # Implement export functionality
        pass
