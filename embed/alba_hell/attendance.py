from alba_hell import app
from alba_hell.model import Attendance
from alba_hell import db
from flask import render_template
from flask import session
from flask import request
import requests
from datetime import datetime

url = 'http://api.qrserver.com/v1/create-qr-code?size=250x250&data='
attendance_check_page = 'http://113.198.245.107:12345/attendance'


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
    app.logger.debug(result.end_time)
    if result:
        if result.end_time:
            return "오늘 근무는 끝입니다."
        else:
            result.end_time = datetime.today()
    else:
        attendance = Attendance(emp_id=id, start_time=datetime.now())
    db.session.commit()
    app.logger.debug(session['store_id'] + " 매장 " + id + "직원 일 시작")
    # app.logger.debug(session['store_id'] + " 매장 " + id + "직원 일 종료")
    return str(session['store_id'])
