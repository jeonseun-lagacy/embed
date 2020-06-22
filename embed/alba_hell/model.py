from embed.alba_hell import db
from datetime import datetime


class Store(db.Model):
    __tablename__ = 'store'
    __table_args__ = {'mysql_collate': 'utf8_general_ci', 'extend_existing': True}

    id = db.Column(db.String(16), primary_key=True)
    manager_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    store_name = db.Column(db.String(20), nullable=False)


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = {'mysql_collate': 'utf8_general_ci', 'extend_existing': True}

    id = db.Column(db.String(16), primary_key=True)
    emp_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    store_id = db.Column(db.String(16), nullable=True, default=None)


class Attendance(db.Model):
    __tablename__ = 'attendance'
    __table_args__ = {'mysql_collate': 'utf8_general_ci', 'extend_existing': True}

    emp_id = db.Column(db.String(16), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    today = db.Column(db.DateTime, default=datetime.today())


if __name__ == "__main__":
    items = Employee.query.all()
    print(items)
    for item in items:
        print(item)
