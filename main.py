import sys
from PyQt5.QtWidgets import QApplication
from src.config.firebase_config import initialize_firebase
from src.gui.main_window import MainWindow

def main():
    # Initialize Firebase
    db = initialize_firebase()

    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow(db)
    window.show()
    
    # Start application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
