from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from my_util.weather import get_weather

rgrs_bp = Blueprint('rgrs_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 
        'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
        'cf':0, 'ac':0, 're':1, 'cu':0, 'nl':0}

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

@rgrs_bp.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'GET':
        return render_template('regression/diabetes.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        feature = request.form['feature']
        df = pd.read_csv('static/data/diabetes_train.csv')
        X = df[feature].values.reshape(-1,1)
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/diabetes_test.csv')
        X_test = df_test[feature][index]
        y_test = df_test.target[index]
        pred = np.round(X_test * weight[0] + bias, 2)

        y_min = np.min(X) * weight[0] + bias
        y_max = np.max(X) * weight[0] + bias
        plt.figure()
        plt.scatter(X, y, label='train')
        plt.plot([np.min(X), np.max(X)], [y_min, y_max], 'r', lw=3)
        plt.scatter([X_test], [y_test], c='r', marker='*', s=100, label='test')
        plt.grid()
        plt.legend()
        plt.title(f'Diabetes target vs. {feature}')
        img_file = os.path.join(current_app.root_path, 'static/img/diabetes.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index, 'feature':feature, 'y':y_test, 'pred':pred}
        return render_template('regression/diabetes_res.html', res=result_dict, mtime=mtime,
                                menu=menu, weather=get_weather())

@rgrs_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    if request.method == 'GET':
        return render_template('regression/iris.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        feature_name = request.form['feature']
        column_dict = {'sl':'Sepal length', 'sw':'Sepal width', 
                       'pl':'Petal length', 'pw':'Petal width', 
                       'species':['Setosa', 'Versicolor', 'Virginica']}
        column_list = list(column_dict.keys())

        df = pd.read_csv('static/data/iris_train.csv')
        df.columns = column_list
        X = df.drop(columns=feature_name, axis=1).values
        y = df[feature_name].values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/iris_test.csv')
        df_test.columns = column_list
        X_test = df_test.drop(columns=feature_name, axis=1).values[index]
        pred_value = np.dot(X_test, weight.T) + bias

        x_test = list(df_test.iloc[index,:-1].values)
        x_test.append(column_dict['species'][int(df_test.iloc[index,-1])])
        org = dict(zip(column_list, x_test))
        pred = dict(zip(column_list[:-1], [0,0,0,0]))
        pred[feature_name] = np.round(pred_value, 2)
        return render_template('regression/iris_res.html', menu=menu, weather=get_weather(),
                                index=index, org=org, pred=pred, feature=column_dict[feature_name])

@rgrs_bp.route('/boston', methods=['GET', 'POST'])
def boston():
    if request.method == 'GET':
        feature_list = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
                        'TAX', 'PTRATIO', 'B', 'LSTAT']
        return render_template('regression/boston.html', feature_list=feature_list,
                               menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        feature_list = request.form.getlist('feature')
        if len(feature_list) == 0:
            feature_list = ['RM', 'LSTAT']
        df = pd.read_csv('static/data/boston_train.csv')
        X = df[feature_list].values
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/boston_test.csv')
        X_test = df_test[feature_list].values[index, :]
        y_test = df_test.target[index]
        pred = np.dot(X_test, weight.T) + bias      # tmp = lr.predict(X_test.reshape(1,-1))
        pred = np.round(pred, 2)                    # pred = np.round(tmp[0])

        result_dict = {'index':index, 'feature':feature_list, 'y':y_test, 'pred':pred}
        org = dict(zip(df.columns[:-1], df_test.iloc[index, :-1]))
        return render_template('regression/boston_res.html', res=result_dict, org=org,
                               menu=menu, weather=get_weather())

kospi_dict, kosdaq_dict, nyse_dict, nasdaq_dict = {}, {}, {}, {}
@rgrs_bp.before_app_first_request
def before_app_first_request():
    kospi = pd.read_csv('./static/data/KOSPI.csv', dtype={'종목코드': str})
    for i in kospi.index:
        kospi_dict[kospi['종목코드'][i]] = kospi['기업명'][i]
    kosdaq = pd.read_csv('./static/data/KOSDAQ.csv', dtype={'종목코드': str})
    for i in kosdaq.index:
        kosdaq_dict[kosdaq['종목코드'][i]] = kosdaq['기업명'][i]
    nyse = pd.read_excel('./static/data/NYSE.xlsx', dtype={'Ticker': str})
    for i in nyse.index:
        nyse_dict[nyse['Ticker'][i]] = nyse['Company'][i]
    nasdaq = pd.read_excel('./static/data/NASDAQ.xlsx', dtype={'Ticker': str})
    for i in nasdaq.index:
        nasdaq_dict[nasdaq['Ticker'][i]] = nasdaq['Company'][i]

@rgrs_bp.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'GET':
        return render_template('regression/stock.html', menu=menu, weather=get_weather(),
                                kospi=kospi_dict, kosdaq=kosdaq_dict, 
                                nyse=nyse_dict, nasdaq=nasdaq_dict)
    else:
        market = request.form['market']
        if market == 'KS':
            code = request.form['kospi_code']
            company = kospi_dict[code]
            code += '.KS'
        elif market == 'KQ':
            code = request.form['kosdaq_code']
            company = kosdaq_dict[code]
            code += '.KQ'
        elif market == 'NY':
            code = request.form['nyse_code']
            company = nyse_dict[code]
        else:
            code = request.form['nasdaq_code']
            company = nasdaq_dict[code]
        learn_period = int(request.form['learn'])
        pred_period = int(request.form['pred'])
        current_app.logger.debug(f'{market}, {code}, {learn_period}, {pred_period}')

        today = datetime.now()
        start_learn = today - timedelta(days=learn_period*365)
        end_learn = today - timedelta(days=1)

        stock_data = pdr.DataReader(code, data_source='yahoo', start=start_learn, end=end_learn)
        current_app.logger.info(f"get stock data: {company}({code})")
        df = pd.DataFrame({'ds': stock_data.index, 'y': stock_data.Close})
        df.reset_index(inplace=True)
        try:
            del df['Date']
        except:
            current_app.logger.error('Date error')

        model = Prophet(daily_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=pred_period)
        forecast = model.predict(future)

        fig = model.plot(forecast);
        img_file = os.path.join(current_app.root_path, 'static/img/stock.png')
        fig.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('regression/stock_res.html', menu=menu, weather=get_weather_main(), 
                                mtime=mtime, company=company, code=code)