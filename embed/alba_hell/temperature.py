from alba_hell import app
from alba_hell.model import Temp
from alba_hell import db
from flask import request
import json
from ast import literal_eval
from flask import session, jsonify

@app.route('/temperature', methods=['post'])
def add_temperature_record():
    j_data = request.get_json()

    data = literal_eval(j_data)
    temp = []
    for key, item in data.items():
        temp.append(item)
    app.logger.debug(temp)
    id = temp[0]
    time = temp[1]
    temperature = temp[2]
    humidity = temp[3]
    temp = Temp(store_id=id, measure_time=time, temp=temperature, humidity=humidity)
    db.session.add(temp)
    db.session.commit()
    return "add success"


@app.route('/temps', methods=['post'])
def get_temps():
    # result = Temp.query.filter_by(id=session['id']).all()
    # result = Temp.query.filter_by(store_id=).all()
    # result = Temp.query.filter_by(store_id=session['id']).all()
    result = Temp.query.filter_by(store_id='test1').all()

    test = []
    web_data = dict()

    for i in result:
        web_data = "{'time' : '%s', 'temperature' : '%s' , 'humidity' : '%s'}" % (i.measure_time, i.temp, i.humidity)
        test1 = {}
        test1['time'] = str(i.measure_time)
        test1['temp'] = i.temp
        test1['humidity'] = i.humidity
        # web_data['time'] = str(i.measure_time)
        # web_data['temperature'] = i.temp
        # web_data['humidity'] = i.humidity
        test.append(test1)
        app.logger.debug(i)
    temp = {'all': test}
    return jsonify(temp)
    # app.logger.debug(result)
    # for i in result:
    #     app.logger.debug(i)
    # return 'hi'