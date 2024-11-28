from datetime import datetime
from src.database.firebase_db import db

class Attendance:
    def __init__(self, employee_id, date, month, year, check_in, check_out=None, total_hours=0):
        self.employee_id = employee_id
        self.date = date
        self.month = month
        self.year = year
        self.check_in = check_in
        self.check_out = check_out
        self.total_hours = total_hours

    @staticmethod
    def add_check_in(employee_id):
        now = datetime.now()
        data = {
            'employee_id': employee_id,
            'date': now.strftime('%Y-%m-%d'),
            'month': now.month,
            'year': now.year,
            'check_in': now.strftime('%H:%M:%S'),
            'check_out': None,
            'total_hours': 0
        }
        try:
            db.collection('Attendance').add(data)
            return True
        except Exception as e:
            print(f"Error adding check-in: {e}")
            return False

    @staticmethod
    def add_check_out(employee_id):
        now = datetime.now()
        try:
            # Get today's attendance record
            attendance = db.collection('Attendance')\
                .where('employee_id', '==', employee_id)\
                .where('date', '==', now.strftime('%Y-%m-%d'))\
                .where('check_out', '==', None)\
                .limit(1)\
                .get()

            if not attendance:
                return False

            doc = attendance[0]
            check_in_time = datetime.strptime(doc.to_dict()['check_in'], '%H:%M:%S')
            check_out_time = now
            total_hours = (check_out_time - check_in_time).total_seconds() / 3600

            # Update the record
            doc.reference.update({
                'check_out': now.strftime('%H:%M:%S'),
                'total_hours': round(total_hours, 2)
            })
            return True
        except Exception as e:
            print(f"Error adding check-out: {e}")
            return False

    @staticmethod
    def get_monthly_attendance(employee_id, month, year):
        try:
            attendance = db.collection('Attendance')\
                .where('employee_id', '==', employee_id)\
                .where('month', '==', month)\
                .where('year', '==', year)\
                .stream()
            return [doc.to_dict() for doc in attendance]
        except Exception as e:
            print(f"Error getting monthly attendance: {e}")
            return []
