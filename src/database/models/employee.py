from datetime import datetime
from src.database.firebase_db import db

class Employee:
    def __init__(self, id, name, major, level, salary_per_hour):
        self.id = id
        self.name = name
        self.major = major
        self.level = level
        self.salary_per_hour = salary_per_hour

    @staticmethod
    def add_employee(data):
        try:
            db.collection('Employee').document(data['id']).set(data)
            return True
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False

    @staticmethod
    def update_employee(id, data):
        try:
            db.collection('Employee').document(id).update(data)
            return True
        except Exception as e:
            print(f"Error updating employee: {e}")
            return False

    @staticmethod
    def delete_employee(id):
        try:
            db.collection('Employee').document(id).delete()
            return True
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False

    @staticmethod
    def get_employee(id):
        try:
            return db.collection('Employee').document(id).get().to_dict()
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None

    @staticmethod
    def get_all_employees():
        try:
            employees = db.collection('Employee').stream()
            return [doc.to_dict() for doc in employees]
        except Exception as e:
            print(f"Error getting all employees: {e}")
            return []
