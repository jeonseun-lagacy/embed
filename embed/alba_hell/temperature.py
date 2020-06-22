from alba_hell import app


@app.route('/temperature/<temperature>/<humidity>')
def add_temperature_record(temperature, humidity):
    print()