from flask import Blueprint, render_template, request, session, g
from flask import current_app, redirect, url_for
from datetime import datetime, timedelta
import os, folium, json
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt 
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

@covid_bp.route('/graph_seq')
def graph():
    mpl.rc('font', family='Malgun Gothic')
    mpl.rc('axes', unicode_minus=False)
    menu = {'ho':0, 'da':1, 'ml':0, 'se':0, 'co':1, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    rows = dm.get_region_items_by_gubun('stdDay, incDec', '합계')
    cdf = pd.DataFrame(rows, columns=['기준일','전국'])
    metro_list = ['서울', '부산', '대구', '인천', '대전', '광주', '울산', '세종', 
                  '경기', '강원', '충북', '충남', '경북', '경남', '전북', '전남', '제주']
    for metro in metro_list:
        results = dm.get_region_items_by_gubun('stdDay, incDec', metro)
        df = pd.DataFrame(results, columns=['기준일', metro])
        cdf = pd.merge(cdf, df, on='기준일')
    cdf['기준일'] = pd.to_datetime(cdf['기준일'])
    cdf.set_index('기준일', inplace=True)

    region_str = '전국 서울 경기 대구'
    region_list = region_str.split()
    img_file = os.path.join(current_app.root_path, 'static/img/covid_seq.png')
    for region in region_list:
        cdf[region].plot(grid=True, figsize=(12,8))
    plt.title('일별 확진자 추이', fontsize=15)
    plt.legend()
    plt.savefig(img_file)
    mtime = int(os.stat(img_file).st_mtime)
    region_str = ', '.join(region for region in region_list)

    return render_template('covid/graph_seq.html', menu=menu, weather=get_weather_main(),
                            mtime=mtime, metro_list=metro_list, region_str=region_str)