from src.database.firebase_db import db
from datetime import datetime

class Salary:
    def __init__(self, month, year, total_hours, salary_per_hour, salary, employee_id):
        self.month = month
        self.year = year
        self.total_hours = total_hours
        self.salary_per_hour = salary_per_hour
        self.salary = salary
        self.employee_id = employee_id

    @staticmethod
    def calculate_salary(employee_id, month, year):
        try:
            # Lấy thông tin nhân viên
            employee_ref = db.collection('Employee').document(employee_id).get()
            if not employee_ref.exists:
                return None
            
            employee_data = employee_ref.to_dict()
            salary_per_hour = employee_data['salary_per_hour']

            # Lấy tất cả bản ghi chấm công trong tháng
            attendance_refs = db.collection('Attendance')\
                .where('employee_id', '==', employee_id)\
                .where('month', '==', month)\
                .where('year', '==', year)\
                .stream()

            total_hours = 0
            for att in attendance_refs:
                att_data = att.to_dict()
                total_hours += att_data.get('total_hours', 0)

            # Tính lương
            salary = total_hours * salary_per_hour

            # Lưu thông tin lương
            salary_data = {
                'month': month,
                'year': year,
                'total_hours': total_hours,
                'salary_per_hour': salary_per_hour,
                'salary': salary,
                'employee_id': employee_id,
                'created_at': datetime.now()
            }

            db.collection('Salary').add(salary_data)
            return salary_data

        except Exception as e:
            print(f"Error calculating salary: {e}")
            return None

    @staticmethod
    def get_salary(employee_id, month, year):
        try:
            salary_ref = db.collection('Salary')\
                .where('employee_id', '==', employee_id)\
                .where('month', '==', month)\
                .where('year', '==', year)\
                .limit(1)\
                .get()

            if not salary_ref:
                return None

            return salary_ref[0].to_dict()

        except Exception as e:
            print(f"Error getting salary: {e}")
            return None

    @staticmethod
    def get_all_salaries(month, year):
        try:
            salaries = db.collection('Salary')\
                .where('month', '==', month)\
                .where('year', '==', year)\
                .stream()

            return [doc.to_dict() for doc in salaries]

        except Exception as e:
            print(f"Error getting all salaries: {e}")
            return []
