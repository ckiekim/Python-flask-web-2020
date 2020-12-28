from flask import Flask, render_template, session, request, g
from datetime import timedelta
import os, json, logging
from logging.config import dictConfig
from bp1_seoul.seoul import seoul_bp
from bp2_covid.covid import covid_bp
from bp3_cartogram.carto import carto_bp
from bp4_crawling.crawl import crawl_bp
from bp5_stock.stock import stock_bp
from bp6_wordcloud.word import word_bp
from my_util.weather import get_weather

app = Flask(__name__)
app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'
app.register_blueprint(seoul_bp, url_prefix='/seoul')
app.register_blueprint(covid_bp, url_prefix='/covid')
app.register_blueprint(carto_bp, url_prefix='/cartogram')
app.register_blueprint(crawl_bp, url_prefix='/crawling')
app.register_blueprint(stock_bp, url_prefix='/stock')
app.register_blueprint(word_bp, url_prefix='/wordcloud')

with open('./logging.json', 'r') as file:
    config = json.load(file)
dictConfig(config)
#app.logger 

def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.info("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
    return weather

@app.route('/')
def index():
    menu = {'ho':1, 'da':0, 'ml':0, 'se':0, 'co':0, 'cg':0, 'cr':0, 'st':0, 'wc':0}
    return render_template('index.html', menu=menu, weather=get_weather_main())

if __name__ == '__main__':
    app.run(debug=True)