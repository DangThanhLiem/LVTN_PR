from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.gui.employee_tab import EmployeeTab
from src.gui.attendance_tab import AttendanceTab
from src.gui.salary_tab import SalaryTab

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Face Recognition Attendance System')
        self.setGeometry(100, 100, 1200, 800)

        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create tabs
        self.employee_tab = EmployeeTab(self.db)
        self.attendance_tab = AttendanceTab(self.db)
        self.salary_tab = SalaryTab(self.db)

        # Add tabs
        tab_widget.addTab(self.employee_tab, "Employee Management")
        tab_widget.addTab(self.attendance_tab, "Attendance")
        tab_widget.addTab(self.salary_tab, "Salary")

        self.setCentralWidget(tab_widget)
