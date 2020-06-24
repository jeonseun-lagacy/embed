from alba_hell import app
from alba_hell.model import Attendance
from alba_hell import db
from alba_hell.model import Employee
from flask import render_template
from flask import session
from flask import request
from flask import jsonify
import requests
from datetime import datetime

url = 'http://api.qrserver.com/v1/create-qr-code?size=250x250&data='
attendance_check_page = 'http://113.198.245.107:12345/attendance'
# attendance_check_page = 'http://192.168.0.58:5000/attendance'


# qr code 요청 라우트
@app.route('/qr-code/<string:store_id>')
def get_qr_code(store_id):
    response = requests.get(url + attendance_check_page + '/' + store_id)
    return response.content


# 출퇴근 확인 페이지 라우트
@app.route('/attendance/<string:store_id>')
def attendance_page(store_id):
    session['store_id'] = store_id
    return render_template("attendance/go_to_work.html")


@app.route('/attendance', methods=['post'])
def check_work():
    id = request.form['id']
    result = Attendance.query.filter_by(today=datetime.today().date()).filter_by(emp_id=id).first()
    app.logger.debug(datetime.today().date())
    if result:
        if result.end_time:
            return "오늘 근무는 끝입니다."
        if not result.end_time:
            Attendance.query.filter_by(emp_id=id).filter_by(today=datetime.today().date()).update(dict(end_time=datetime.today()))
            app.logger.debug(session['store_id'] + " 매장 " + id + "직원 일 종료")
            db.session.commit()
            return "근무 종료 !!"
    if not result:
        attendance = Attendance(emp_id=id, start_time=datetime.now())
        db.session.add(attendance)
        db.session.commit()
        app.logger.debug(session['store_id'] + " 매장 " + id + "직원 일 시작")

    return str(session['store_id'])


@app.route('/attendances', methods=['post'])
def get_work_time():
    store_id = session['id']
    # store_id = 'test1'
    store_emp = Employee.query.filter_by(store_id=store_id).all()
    work_data = dict()
    for i in store_emp:
        emp_id = i.id
        app.logger.debug(emp_id)
        attendance_rs = Attendance.query.filter_by(emp_id=emp_id).all()
        work_data[i.id] = []
        for i in attendance_rs:
            work_data[i.emp_id].append(int(str(i.end_time - i.start_time)[0:1]))
    return jsonify(work_data)
