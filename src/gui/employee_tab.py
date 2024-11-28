from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from src.recognition.face_recognition import FaceRecognitionSystem

class EmployeeTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.face_recognition = FaceRecognitionSystem()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Form nhập thông tin nhân viên
        form_group = QGroupBox("Employee Information")
        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.major_input = QLineEdit()
        self.level_input = QLineEdit()
        self.salary_input = QLineEdit()

        form_layout.addRow("ID:", self.id_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Major:", self.major_input)
        form_layout.addRow("Level:", self.level_input)
        form_layout.addRow("Salary/Hour:", self.salary_input)

        # Nút chụp ảnh
        self.capture_btn = QPushButton("Capture Face")
        self.capture_btn.clicked.connect(self.capture_face)
        form_layout.addRow(self.capture_btn)

        form_group.setLayout(form_layout)

        # Bảng danh sách nhân viên
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Major", "Level", "Salary/Hour", "Actions"])

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Employee")
        update_btn = QPushButton("Update")
        delete_btn = QPushButton("Delete")

        add_btn.clicked.connect(self.add_employee)
        update_btn.clicked.connect(self.update_employee)
        delete_btn.clicked.connect(self.delete_employee)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)

        layout.addWidget(form_group)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_employees()

    def capture_face(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Capture Face - Press SPACE to capture', frame)
            
            if cv2.waitKey(1) & 0xFF == ord(' '):
                # Save image
                employee_id = self.id_input.text()
                cv2.imwrite(f'data/employee_images/{employee_id}.jpg', frame)
                break

        cap.release()
        cv2.destroyAllWindows()

    def add_employee(self):
        employee_data = {
            'id': self.id_input.text(),
            'name': self.name_input.text(),
            'major': self.major_input.text(),
            'level': self.level_input.text(),
            'salary_per_hour': float(self.salary_input.text())
        }

        try:
            self.db.collection('Employee').document(employee_data['id']).set(employee_data)
            self.load_employees()
            self.clear_form()
            QMessageBox.information(self, "Success", "Employee added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding employee: {str(e)}")

    def update_employee(self):
        # Similar to add_employee but with update operation
        pass

    def delete_employee(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            employee_id = self.table.item(current_row, 0).text()
            reply = QMessageBox.question(self, 'Delete Employee', 
                                       'Are you sure you want to delete this employee?',
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                try:
                    self.db.collection('Employee').document(employee_id).delete()
                    self.load_employees()
                    QMessageBox.information(self, "Success", "Employee deleted successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error deleting employee: {str(e)}")

    def load_employees(self):
        try:
            employees = self.db.collection('Employee').get()
            self.table.setRowCount(0)
            for employee in employees:
                data = employee.to_dict()
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(data['id']))
                self.table.setItem(row, 1, QTableWidgetItem(data['name']))
                self.table.setItem(row, 2, QTableWidgetItem(data['major']))
                self.table.setItem(row, 3, QTableWidgetItem(data['level']))
                self.table.setItem(row, 4, QTableWidgetItem(str(data['salary_per_hour'])))
                
                # Add edit/delete buttons
                btn_widget = QWidget()
                btn_layout = QHBoxLayout()
                edit_btn = QPushButton("Edit")
                delete_btn = QPushButton("Delete")
                btn_layout.addWidget(edit_btn)
                btn_layout.addWidget(delete_btn)
                btn_widget.setLayout(btn_layout)
                self.table.setCellWidget(row, 5, btn_widget)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading employees: {str(e)}")

    def clear_form(self):
        self.id_input.clear()
        self.name_input.clear()
        self.major_input.clear()
        self.level_input.clear()
        self.salary_input.clear()
