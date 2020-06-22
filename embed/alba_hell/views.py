from alba_hell import app
from flask import render_template
from flask import session
from flask import redirect


@app.route('/')
def index_page():
    if 'id' in session:
        return redirect('/main')
    return render_template('index.html')


@app.route('/sign-up')
def sign_up_page():
    return render_template('sign_up.html')


@app.route('/main')
def main_page():
    if session['type'] == 'admin':
        return render_template('admin_main.html')
    else:
        return render_template('emp_main.html')
