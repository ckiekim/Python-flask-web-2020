from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
import os
import pandas as pd
from my_util.weather import get_weather

crawl_bp = Blueprint('crawl_bp', __name__)

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

@crawl_bp.route('/food')
def food():
    pass

@crawl_bp.route('/music')
def music():
    pass