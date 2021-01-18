from flask import Blueprint, render_template, request, session
from flask import current_app, redirect, url_for
from fbprophet import Prophet
from datetime import datetime, timedelta
import os
import pandas as pd
from my_util.weather import get_weather
import my_util.crawl_util as cu

crawl_bp = Blueprint('crawl_bp', __name__)

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

@crawl_bp.route('/food', methods=['GET', 'POST'])
def food():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':1, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    if request.method == 'GET':
        place = request.args.get('place', '발산역')
        rest_list = cu.siksin(place)
        return render_template('crawling/food.html', menu=menu, weather=get_weather(),
                                rest_list=rest_list, place=place)
    else:
        place = request.form['place']
        return redirect(url_for('crawl_bp.food')+f'?place={place}')

@crawl_bp.route('/music')
def music():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':1, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    music_list = cu.genie()
    return render_template('crawling/music.html', menu=menu, weather=get_weather(),
                            music_list=music_list)

@crawl_bp.route('/music_jquery')
def music_jquery():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':1, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    music_list = cu.genie()
    return render_template('crawling/music_jquery.html', menu=menu, weather=get_weather(),
                            music_list=music_list)

@crawl_bp.route('/book')
def book():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':1, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    book_list = cu.interpark()
    return render_template('crawling/book.html', menu=menu, weather=get_weather(),
                            book_list=book_list)
