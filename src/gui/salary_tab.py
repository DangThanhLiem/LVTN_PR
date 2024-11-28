from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from datetime import datetime

class SalaryTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Filter options
        filter_group = QGroupBox("Filter")
        filter_layout = QHBoxLayout()

        # Month selection
        self.month_combo = QComboBox()
        self.month_combo.addItems([str(i) for i in range(1, 13)])
        
        # Year selection
        self.year_combo = QComboBox()
        current_year = datetime.now().year
        self.year_combo.addItems([str(i) for i in range(current_year-5, current_year+1)])

        # Employee selection
        self.employee_combo = QComboBox()
        self.load_employees()

        filter_layout.addWidget(QLabel("Month:"))
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(QLabel("Year:"))
        filter_layout.addWidget(self.year_combo)
        filter_layout.addWidget(QLabel("Employee:"))
        filter_layout.addWidget(self.employee_combo)

        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        # Salary table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Employee ID", "Name", "Month", "Total Hours", "Rate/Hour", "Total Salary"])
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        calculate_btn = QPushButton("Calculate Salary")
        export_btn = QPushButton("Export Report")

        calculate_btn.clicked.connect(self.calculate_salary)
        export_btn.clicked.connect(self.export_report)

        btn_layout.addWidget(calculate_btn)
        btn_layout.addWidget(export_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_employees(self):
        try:
            employees = self.db.collection('Employee').get()
            self.employee_combo.clear()
            self.employee_combo.addItem("All Employees")
            for employee in employees:
                data = employee.to_dict()
                self.employee_combo.addItem(f"{data['id']} - {data['name']}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading employees: {str(e)}")

    def calculate_salary(self):
        try:
            month = int(self.month_combo.currentText())
            year = int(self.year_combo.currentText())
            employee_filter = self.employee_combo.currentText()

            # Clear table
            self.table.setRowCount(0)

            # Get attendance records
            if employee_filter == "All Employees":
                attendance_docs = self.db.collection('Attendance')\
                    .where('month', '==', month)\
                    .where('year', '==', year)\
                    .get()
            else:
                employee_id = employee_filter.split(' - ')[0]
                attendance_docs = self.db.collection('Attendance')\
                    .where('employee_id', '==', employee_id)\
                    .where('month', '==', month)\
                    .where('year', '==', year)\
                    .get()

            # Calculate salary for each employee
            salary_data = {}
            for doc in attendance_docs:
                data = doc.to_dict()
                employee_id = data['employee_id']
                
                if employee_id not in salary_data:
                    salary_data[employee_id] = {
                        'total_hours': 0,
                        'employee_data': None
                    }
                
                salary_data[employee_id]['total_hours'] += data['total_hours']
                
                if salary_data[employee_id]['employee_data'] is None:
                    employee_doc = self.db.collection('Employee')\
                        .document(employee_id).get()
                    salary_data[employee_id]['employee_data'] = employee_doc.to_dict()

            # Display results
            for employee_id, data in salary_data.items():
                employee_data = data['employee_data']
                total_hours = data['total_hours']
                rate = employee_data['salary_per_hour']
                total_salary = total_hours * rate

                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(employee_id))
                self.table.setItem(row, 1, QTableWidgetItem(employee_data['name']))
                self.table.setItem(row, 2, QTableWidgetItem(f"{month}/{year}"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{total_hours:.2f}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"${rate:.2f}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"${total_salary:.2f}"))

                # Save salary record to database
                salary_record = {
                    'employee_id': employee_id,
                    'month': month,
                    'year': year,
                    'total_hours': total_hours,
                    'salary_per_hour': rate,
                    'total_salary': total_salary
                }
                self.db.collection('Salary').add(salary_record)

            QMessageBox.information(self, "Success", "Salary calculation completed!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calculating salary: {str(e)}")

    def export_report(self):
        try:
            # Get current filter settings
            month = int(self.month_combo.currentText())
            year = int(self.year_combo.currentText())
            
            # Create data for export
            data = []
            for row in range(self.table.rowCount()):
                row_data = {
                    'Employee ID': self.table.item(row, 0).text(),
                    'Name': self.table.item(row, 1).text(),
                    'Period': self.table.item(row, 2).text(),
                    'Total Hours': float(self.table.item(row, 3).text()),
                    'Rate/Hour': float(self.table.item(row, 4).text().replace('$', '')),
                    'Total Salary': float(self.table.item(row, 5).text().replace('$', ''))
                }
                data.append(row_data)

            # Create DataFrame
            df = pd.DataFrame(data)

            # Get save file name
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Export Salary Report",
                f"salary_report_{month}_{year}.xlsx",
                "Excel Files (*.xlsx);;CSV Files (*.csv)"
            )

            if file_name:
                if file_name.endswith('.xlsx'):
                    # Export to Excel
                    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                    df.to_excel(writer, sheet_name='Salary Report', index=False)
                    
                    # Get workbook and worksheet objects
                    workbook = writer.book
                    worksheet = writer.sheets['Salary Report']
                    
                    # Add formats
                    money_format = workbook.add_format({'num_format': '$#,##0.00'})
                    header_format = workbook.add_format({
                        'bold': True,
                        'bg_color': '#D3D3D3',
                        'border': 1
                    })
                    
                    # Apply formats
                    worksheet.set_column('E:F', 12, money_format)  # Apply money format to salary columns
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                    
                    # Auto-adjust columns width
                    for i, col in enumerate(df.columns):
                        column_len = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                        worksheet.set_column(i, i, column_len)
                    
                    writer.close()
                else:
                    # Export to CSV
                    df.to_csv(file_name, index=False)

                QMessageBox.information(self, "Success", f"Report exported successfully to {file_name}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting report: {str(e)}")

    def update_salary_display(self):
        """Update the salary display when filters change"""
        self.calculate_salary()

    def format_currency(self, value):
        """Format number as currency"""
        return f"${value:,.2f}"

    def get_employee_details(self, employee_id):
        """Get employee details from database"""
        try:
            doc = self.db.collection('Employee').document(employee_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            print(f"Error getting employee details: {str(e)}")
            return None

    def clear_table(self):
        """Clear the salary table"""
        self.table.setRowCount(0)

    def refresh_data(self):
        """Refresh all data in the tab"""
        self.load_employees()
        self.calculate_salary()

