from flask import Blueprint, render_template, request, session, g
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import timedelta
import os, folium, json
import pandas as pd
from my_util.weather import get_weather
from my_util.wordCloud import engCloud, hanCloud
from my_util.sports_news import get_sports_news

word_bp = Blueprint('word_bp', __name__)

def get_weather_main():
    ''' weather = None
    try:
        weather = session['weather']
    except:
        current_app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=60) '''
    weather = get_weather()
    return weather

@word_bp.route('/text', methods=['GET', 'POST'])
def text():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':1,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    if request.method == 'GET':
        return render_template('wordcloud/text.html', menu=menu, weather=get_weather_main())
    else:
        lang = request.form['lang']
        f_text = request.files['text']
        file_text = os.path.join(current_app.root_path, 'static/upload/') + f_text.filename
        f_text.save(file_text)
        if request.files['mask']:
            f_mask = request.files['mask']
            file_mask = os.path.join(current_app.root_path, 'static/upload/') + f_mask.filename
            f_mask.save(file_mask)
        else:
            file_mask = None
        stop_words = request.form['stop_words']
        current_app.logger.debug(f"{lang}, {f_text}, {request.files['mask']}, {stop_words}")

        text = open(file_text, encoding='utf-8').read()
        stop_words = stop_words.split(' ') if stop_words else []
        img_file = os.path.join(current_app.root_path, 'static/img/text.png')
        if lang == 'en':
            engCloud(text, stop_words, file_mask, img_file)
        else:
            hanCloud(text, stop_words, file_mask, img_file)

        mtime = int(os.stat(img_file).st_mtime)
        return render_template('wordcloud/text_res.html', menu=menu, weather=get_weather_main(),
                                filename=f_text.filename, mtime=mtime)

@word_bp.route('/sports_news')
def sports_news():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':1,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    text_file = os.path.join(current_app.root_path, 'static/data/sports.txt')
    get_sports_news(text_file)

    text = open(text_file, encoding='utf-8').read()
    stop_words = ['오피셜']
    mask_file = os.path.join(current_app.root_path, 'static/img/ball.jpg')
    img_file = os.path.join(current_app.root_path, 'static/img/sports.png')
    hanCloud(text, stop_words, mask_file, img_file)
    mtime = int(os.stat(img_file).st_mtime)
    return render_template('wordcloud/sports_res.html', menu=menu, weather=get_weather_main(),
                            mtime=mtime)