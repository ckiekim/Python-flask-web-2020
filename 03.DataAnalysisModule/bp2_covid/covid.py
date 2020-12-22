from flask import Blueprint, render_template, request, session, g
from flask import current_app, redirect, url_for
from datetime import datetime, timedelta
import os, folium, json
import pandas as pd
from my_util.weather import get_weather
import db.db_module as dm
import my_util.covid_util as cu

covid_bp = Blueprint('covid_bp', __name__)

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

@covid_bp.route('/daily')
def daily():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_region_daily(date)

    return render_template('covid/daily.html', menu=menu, weather=get_weather_main(),
                            date=date, rows=rows)

@covid_bp.route('/update_region/<date>')
def update_region(date):
    rows = dm.get_region_daily(date)
    if len(rows) == 0:
        cu.get_region_by_date(date)

    return redirect(url_for('covid_bp.daily')+f'?date={date}')

@covid_bp.route('/agender')
def agender():
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    rows = dm.get_agender_daily(date)

    return render_template('covid/agender.html', menu=menu, weather=get_weather_main(),
                            date=date, rows=rows)

@covid_bp.route('/update_agender/<date>')
def update_agender(date):
    rows = dm.get_agender_daily(date)
    if len(rows) == 0:
        cu.get_agender_by_date(date)

    return redirect(url_for('covid_bp.agender')+f'?date={date}')