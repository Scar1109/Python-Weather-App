from flask import Flask, render_template, request
from weather import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        city_name = request.form['cityName']
        state_name = request.form['stateName']
        country_name = request.form['countryName']
        data = main(city_name, state_name, country_name)
        print(data)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
