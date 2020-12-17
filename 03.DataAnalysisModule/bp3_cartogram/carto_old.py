from flask import Blueprint, render_template, request, session
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import timedelta
import os, json
import pandas as pd
from my_util.weather import get_weather

carto_bp = Blueprint('carto_bp', __name__)

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@carto_bp.route('/coffee', methods=['GET', 'POST'])
def coffee():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':0, 'cg':1, 'cr':0, 'st':0, 'wc':0}
    if request.method == 'GET':
        return render_template('cartogram/coffee.html', menu=menu, weather=get_weather_main())
    else:
        item = request.form['item']
        f = request.files['csv']
        filename = os.path.join(current_app.root_path, 'static/upload/') + f.filename
        f.save(filename)
        current_app.logger.info(f'{filename} is saved.')
        df = pd.read_csv(filename, index_col='ID')
        return filename
