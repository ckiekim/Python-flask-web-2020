from flask import Flask, render_template
from my_util.weather import get_weather
app = Flask(__name__)

@app.route('/')
def index():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':0, 'cg':0, 'cr':0, 'st':1, 'wc':0}
    weather = get_weather()
    return render_template('09.main.html', menu=menu, weather=weather)

@app.route('/park')
def park():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':1, 'co':0, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    pass

if __name__ == '__main__':
    app.run(debug=True)