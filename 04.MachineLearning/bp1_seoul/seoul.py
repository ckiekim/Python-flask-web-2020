from flask import Blueprint, render_template, request, session, g
from flask import current_app
from datetime import timedelta
import os, folium, json
import numpy as np
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt
from my_util.weather import get_weather

seoul_bp = Blueprint('seoul_bp', __name__)

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

@seoul_bp.route('/park', methods=['GET', 'POST'])
def park():
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':1, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    park_new = pd.read_csv('./static/data/park_info.csv')
    park_gu = pd.read_csv('./static/data/park_gu.csv')
    park_gu.set_index('지역', inplace=True)
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        for i in park_new.index:
            folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                                radius=int(park_new['size'][i]),
                                tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                                color='#3186cc', fill_color='#3186cc').add_to(map)
        html_file = os.path.join(current_app.root_path, 'static/img/park.html')
        map.save(html_file)
        mtime = int(os.stat(html_file).st_mtime)
        return render_template('seoul/park.html', menu=menu, weather=get_weather_main(),
                                park_list=list(park_new['공원명'].sort_values()), 
                                gu_list=list(park_gu.index), mtime=mtime)
    else:
        gubun = request.form['gubun']
        if gubun == 'park':
            park_name = request.form['name']
            df = park_new[park_new['공원명'] == park_name].reset_index()
            park_result = {'name':park_name, 'addr':df['공원주소'][0], 
                            'area':int(df.area[0]), 'desc':df['공원개요'][0]}
            map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
            for i in park_new.index:
                folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                                    radius=int(park_new['size'][i]),
                                    tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                                    color='#3186cc', fill_color='#3186cc').add_to(map)
            folium.CircleMarker([df.lat[0], df.lng[0]], radius=int(df['size'][0]),
                                    tooltip=f"{df['공원명'][0]}({int(df.area[0])}㎡)",
                                    color='crimson', fill_color='crimson').add_to(map)
            html_file = os.path.join(current_app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('seoul/park_res.html', menu=menu, weather=get_weather_main(),
                                    park_result=park_result, mtime=mtime)
        else:
            gu_name = request.form['gu']
            df = park_gu[park_gu.index == gu_name].reset_index()
            park_result = {'gu':df['지역'][0], 
                            'area':int(df['공원면적'][0]), 'm_area':int(park_gu['공원면적'].mean()),
                            'count':df['공원수'][0], 'm_count':round(park_gu['공원수'].mean(),1),
                            'area_ratio':round(df['공원면적비율'][0],2), 'm_area_ratio':round(park_gu['공원면적비율'].mean(),2),
                            'per_person':round(df['인당공원면적'][0],2), 'm_per_person':round(park_gu['인당공원면적'].mean(),2)}
            df = park_new[park_new['지역'] == gu_name].reset_index()
            map = folium.Map(location=[df.lat.mean(), df.lng.mean()], zoom_start=13)
            for i in df.index:
                folium.CircleMarker([df.lat[i], df.lng[i]], 
                                    radius=int(df['size'][i])*3,
                                    tooltip=f"{df['공원명'][i]}({int(df.area[i])}㎡)",
                                    color='#3186cc', fill_color='#3186cc').add_to(map)
            html_file = os.path.join(current_app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('seoul/park_res2.html', menu=menu, weather=get_weather_main(),
                                    park_result=park_result, mtime=mtime)

@seoul_bp.route('/park_gu/<option>')
def park_gu(option):
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':1, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    park_new = pd.read_csv('./static/data/park_info.csv')
    park_gu = pd.read_csv('./static/data/park_gu.csv')
    park_gu.set_index('지역', inplace=True)
    geo_str = json.load(open('./static/data/skorea_municipalities_geo_simple.json',
                         encoding='utf8'))
    option_dict = {'area':'공원면적', 'count':'공원수', 'area_ratio':'공원면적 비율', 'per_person':'인당 공원면적'}
    column_index = option_dict[option].replace(' ','')
    
    map = folium.Map(location=[37.5502, 126.982], zoom_start=11, tiles='Stamen Toner')
    map.choropleth(geo_data = geo_str, data = park_gu[column_index],
                    columns = [park_gu.index, park_gu[column_index]],
                    fill_color = 'PuRd', key_on = 'feature.id')
    for i in park_new.index:
        folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                        radius=int(park_new['size'][i]),
                        tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                        color='green', fill_color='green').add_to(map)
    html_file = os.path.join(current_app.root_path, 'static/img/park_gu.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    return render_template('seoul/park_gu.html', menu=menu, weather=get_weather_main(),
                            option=option, option_dict=option_dict, mtime=mtime)

@seoul_bp.route('/crime/<option>')
def crime(option):
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':1, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    crime = pd.read_csv('./static/data/crime.csv', index_col='구별')
    police = pd.read_csv('./static/data/police.csv')
    geo_str = json.load(open('./static/data/skorea_municipalities_geo_simple.json',
                         encoding='utf8'))
    option_dict = {'crime':'범죄', 'murder':'살인', 'rob':'강도', 'rape':'강간', 'thief':'절도', 'violence':'폭력',
                   'arrest':'검거율', 'a_murder':'살인검거율', 'a_rob':'강도검거율', 'a_rape':'강간검거율', 
                   'a_thief':'절도검거율', 'a_violence':'폭력검거율'}
    current_app.logger.debug(option_dict[option])

    map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
    if option in ['crime', 'murder', 'rob', 'rape', 'thief', 'violence']:
        map.choropleth(geo_data = geo_str, data = crime[option_dict[option]],
               columns = [crime.index, crime[option_dict[option]]],
               fill_color = 'PuRd', key_on = 'feature.id')
    else:
        map.choropleth(geo_data = geo_str, data = crime[option_dict[option]],
               columns = [crime.index, crime[option_dict[option]]],
               fill_color = 'YlGnBu', key_on = 'feature.id')
        for i in police.index:
            folium.CircleMarker([police.lat[i], police.lng[i]], radius=10,
                                tooltip=police['관서명'][i],
                                color='crimson', fill_color='crimson').add_to(map)

    html_file = os.path.join(current_app.root_path, 'static/img/crime.html')
    map.save(html_file)
    mtime = int(os.stat(html_file).st_mtime)
    return render_template('seoul/crime.html', menu=menu, weather=get_weather_main(),
                            option=option, option_dict=option_dict, mtime=mtime)

@seoul_bp.route('/cctv/<option>')
def cctv(option):
    menu = {'ho':0, 'da':1, 'ml':0, 
            'se':1, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    df = pd.read_csv('./static/data/cctv.csv')
    df.set_index('구별', inplace=True)
    df_sort = df.sort_values('오차', ascending=False)

    if option == 'graph':
        fp1 = np.polyfit(df['인구수'], df['소계'], 1)
        fx = np.array([100000, 700000])
        f1 = np.poly1d(fp1)
        fy = f1(fx)

        plt.figure(figsize=(12,8))
        plt.scatter(df['인구수'], df['소계'], c=df['오차'], s=50)
        plt.plot(fx, fy, ls='dashed', lw=3, color='g')

        for i in range(10): 
            plt.text(df_sort['인구수'][i]+5000, df_sort['소계'][i]-50,
                    df_sort.index[i], fontsize=15)

        plt.grid(True)
        plt.title('인구수와 CCTV 댓수의 관계', fontsize=20)
        plt.xlabel('인구수')
        plt.ylabel('CCTV')
        plt.colorbar()
        img_file = os.path.join(current_app.root_path, 'static/img/cctv.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('seoul/cctv.html', menu=menu, weather=get_weather_main(), 
                                mtime=mtime)

    else:
        tbl = []
        for i in range(25):
            row =  {'idx':df.index[i], 'number':df['소계'][i], 'inc':df['최근증가율'][i], 
                    'population':df['인구수'][i], 'ratio':df['cctv비율'][i]}
            tbl.append(row)
        return render_template('seoul/cctv_table.html', menu=menu, weather=get_weather_main(), 
                                tbl=tbl)
