from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import os, joblib
import pandas as pd
from my_util.weather import get_weather

clsf_bp = Blueprint('clsf_bp', __name__)

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

@clsf_bp.route('/titanic', methods=['GET', 'POST'])
def titanic():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0}
    if request.method == 'GET':
        return render_template('classification/titanic.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/titanic_test.csv')
        scaler = joblib.load('static/model/titanic_scaler.pkl')
        data = df.iloc[index, 1:].values.reshape(1,-1)
        test_data = scaler.transform(data)
        label = df.iloc[index, 0]
        lrc = joblib.load('static/model/titanic_lr.pkl')
        svc = joblib.load('static/model/titanic_sv.pkl')
        rfc = joblib.load('static/model/titanic_rf.pkl')
        pred_lr = lrc.predict(test_data)
        pred_sv = svc.predict(test_data)
        pred_rf = rfc.predict(test_data)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}

        tmp = df.iloc[index, 1:].values
        value_list = []
        int_index_list = [0, 1, 3, 4, 6, 7]
        for i in range(8):
            if i in int_index_list:
                value_list.append(int(tmp[i]))
            else:
                value_list.append(tmp[i])
        org = dict(zip(df.columns[1:], value_list))
        return render_template('classification/titanic_res.html', menu=menu, 
                                res=result, org=org, weather=get_weather())

@clsf_bp.route('/pima', methods=['GET', 'POST'])
def pima():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0}
    if request.method == 'GET':
        return render_template('classification/pima.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/pima_test.csv')
        scaler = joblib.load('static/model/pima_scaler.pkl')
        data = df.iloc[index, :-1].values.reshape(1,-1)
        test_data = scaler.transform(data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/pima_lr.pkl')
        svc = joblib.load('static/model/pima_sv.pkl')
        rfc = joblib.load('static/model/pima_rf.pkl')
        pred_lr = lrc.predict(test_data)
        pred_sv = svc.predict(test_data)
        pred_rf = rfc.predict(test_data)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classification/pima_res.html', menu=menu, 
                                res=result, org=org, weather=get_weather())

@clsf_bp.route('/cancer', methods=['GET', 'POST'])
def cancer():
    menu = {'ho':0, 'da':0, 'ml':10, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0}
    if request.method == 'GET':
        return render_template('classification/cancer.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/cancer_test.csv')
        scaler = joblib.load('static/model/cancer_scaler.pkl')
        data = df.iloc[index, :-1].values.reshape(1,-1)
        test_data = scaler.transform(data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/cancer_lr.pkl')
        svc = joblib.load('static/model/cancer_sv.pkl')
        rfc = joblib.load('static/model/cancer_rf.pkl')
        pred_lr = lrc.predict(test_data)
        pred_sv = svc.predict(test_data)
        pred_rf = rfc.predict(test_data)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classification/cancer_res.html', menu=menu, 
                                res=result, org=org, weather=get_weather())
