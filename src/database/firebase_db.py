from datetime import datetime
from typing import Dict, List

class FirebaseDB:
    def __init__(self, db):
        self.db = db

    # Employee Operations
    def add_employee(self, employee_data: Dict):
        return self.db.collection('Employee').add(employee_data)

    def update_employee(self, employee_id: str, data: Dict):
        return self.db.collection('Employee').document(employee_id).update(data)

    def delete_employee(self, employee_id: str):
        return self.db.collection('Employee').document(employee_id).delete()

    def get_all_employees(self) -> List[Dict]:
        docs = self.db.collection('Employee').stream()
        return [{**doc.to_dict(), 'id': doc.id} for doc in docs]

    # Attendance Operations
    def check_in(self, employee_id: str):
        now = datetime.now()
        attendance_data = {
            'employee_id': employee_id,
            'date': now.date().isoformat(),
            'month': now.month,
            'year': now.year,
            'check_in': now.strftime('%H:%M:%S'),
            'check_out': None,
            'total_hours': 0
        }
        return self.db.collection('Attendance').add(attendance_data)

    def check_out(self, attendance_id: str):
        now = datetime.now()
        doc_ref = self.db.collection('Attendance').document(attendance_id)
        check_in_time = datetime.strptime(doc_ref.get().to_dict()['check_in'], '%H:%M:%S')
        total_hours = (now - check_in_time).total_seconds() / 3600

        return doc_ref.update({
            'check_out': now.strftime('%H:%M:%S'),
            'total_hours': round(total_hours, 2)
        })

    # Salary Operations
    def calculate_salary(self, employee_id: str, month: int, year: int):
        # Get employee's salary per hour
        employee = self.db.collection('Employee').document(employee_id).get().to_dict()
        salary_per_hour = employee['salary_per_hour']

        # Get total hours worked
        attendance_docs = self.db.collection('Attendance')\
            .where('employee_id', '==', employee_id)\
            .where('month', '==', month)\
            .where('year', '==', year)\
            .stream()

        total_hours = sum(doc.to_dict()['total_hours'] for doc in attendance_docs)
        total_salary = total_hours * salary_per_hour

        # Save salary record
        salary_data = {
            'employee_id': employee_id,
            'month': month,
            'year': year,
            'total_hours': total_hours,
            'salary_per_hour': salary_per_hour,
            'salary': total_salary
        }
        return self.db.collection('Salary').add(salary_data)
