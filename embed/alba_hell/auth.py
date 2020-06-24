from alba_hell import app
from alba_hell import db
from alba_hell.model import Store
from alba_hell.model import Employee
from flask import request
from flask import redirect
from flask import jsonify
from flask import session
from flask import render_template


@app.route('/login', methods=['post'])
def login():
    id = request.form['id']
    password = request.form['password']
    app.logger.debug("id : " + id)
    app.logger.debug("password : " + password)
    manager_result = Store.query.filter_by(id=id).filter_by(password=password).first()
    if manager_result:
        session['id'] = manager_result.id
        session['type'] = 'admin'
        app.logger.debug("current user is admin : " + session['id'])
        return redirect('/main')
    else:
        emp_result = Employee.query.filter_by(id=id).filter_by(password=password).first()
        if emp_result:
            session['id'] = emp_result.id
            session['type'] = 'employee'
            app.logger.debug("current user is employee : " + session['id'])
            return redirect('/main')
        else:
            app.logger.debug("login failed")
        return redirect('/')


@app.route('/logout', methods=['get'])
def logout():
    if 'id' in session:
        app.logger.debug(session['id'] + " logout")
        session.pop('type', None)
        session.pop('id', None)
    return redirect('/')


@app.route('/id', methods=['post'])
def id_check():
    data = request.get_json()
    id = data['id']
    app.logger.debug("new id :" + id)
    result1 = Store.query.filter_by(id=id).first()
    result2 = Employee.query.filter_by(id=id).first()
    app.logger.debug("exist store id list :" + str(result1))
    app.logger.debug("exist emp id list :" + str(result2))
    if not result1 and not result2:
        app.logger.info(id + ' 사용가능')
        return jsonify({'existence': 'false'})
    else:
        app.logger.info(id + ' 사용불가')
        return jsonify({'existence': 'true'})


@app.route('/user', methods=['post'])
def sign_up_manager():
    id = request.form['id']
    manager_name = request.form['manager_name']
    password = request.form['password']
    store_name = request.form['store_name']
    store = Store(id=id, manager_name=manager_name, password=password, store_name=store_name)
    db.session.add(store)
    db.session.commit()
    app.logger.debug("new store added, store : " + store_name)
    app.logger.debug("new store added, manager : " + manager_name)
    # app.logger.debug("new store added, location: " + manager_name)
    return redirect('/')


@app.route('/user/employee', methods=['post'])
def sign_up_emp():
    id = request.form['id']
    emp_name = request.form['emp_name']
    password = request.form['password']
    app.logger.debug("emp : " + id + emp_name + password)
    emp = Employee(id=id, emp_name=emp_name, password=password)
    db.session.add(emp)
    db.session.commit()
    return redirect('/')


@app.route('/management')
def show_emp_list():
    items = Employee.query.all()
    app.logger.info(session['id'])
    for item in items:
        app.logger.debug(item)

    return render_template("admin_manage_menu.html", items=items)


@app.route('/user/register/<emp_id>')
def register_emp(emp_id):
    is_success = False
    app.logger.info(session['id'])
    try:
        Employee.query.filter_by(id=emp_id).update({"store_id": session['id']})
        db.session.commit()
        is_success = True
        return "success"
    except Exception as ex:
        app.logger.debug(ex)

    return "failed"


@app.route('/store', methods=['post'])
def get_store_info():
    id = session['id']
    rs = Store.query.filter_by(id=id).first()
    app.logger.debug(rs.id)
    app.logger.debug(rs.manager_name)
    app.logger.debug(rs.store_name)
    store_data = {
        "store_name": rs.store_name,
        "manager_name": rs.manager_name
    }
    return jsonify(store_data)