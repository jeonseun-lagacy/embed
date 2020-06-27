from flask import request 
from flask import Flask
import MySQLdb
import json
import ast

app = Flask(__name__)

@app.route('/temperature', methods=['POST'])
def index():
    if request.method == 'POST':
        print(request.get_json())

        data = request.get_json()
        d_data = ast.literal_eval(data)

        data_parse=[]
        for key, item in d_data.items():
            data_parse.append(item)
        
        db = MySQLdb.connect("localhost", "root", "", "test")

        cur = db.cursor()
        temp = "insert into temperature values('%s','%s', '%s','%s')" % (data_parse[0], data_parse[1], data_parse[2], data_parse[3]) 
        cur.execute(temp)
        db.commit()

        cur.close()
        db.close()

        return str(request.get_json())

if __name__ == '__main__' :
    app.run(host='localhost', port=8080)
