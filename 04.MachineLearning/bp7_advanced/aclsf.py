from flask import Blueprint, render_template, request, session, g
from flask import current_app
from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.datasets import load_digits
from konlpy.tag import Okt
import os, re, joblib
import pandas as pd
import matplotlib.pyplot as plt
from my_util.weather import get_weather

aclsf_bp = Blueprint('aclsf_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 
        'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
        'cf':0, 'ac':1, 're':0, 'cu':0}

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

@aclsf_bp.before_app_first_request
def before_app_first_request():
    #global imdb_count_lr, imdb_tfidf_lr
    global naver_count_lr, naver_count_nb, naver_tfidf_lr, naver_tfidf_nb
    #global news_count_lr, news_tfidf_lr, news_tfidf_sv
    print('============ Advanced Blueprint before_app_first_request() ==========')
    ''' imdb_count_lr = joblib.load('static/model/imdb_count_lr.pkl')
    imdb_tfidf_lr = joblib.load('static/model/imdb_tfidf_lr.pkl') '''
    naver_count_lr = joblib.load('static/model/naver_count_lr.pkl')
    naver_count_nb = joblib.load('static/model/naver_count_nb.pkl')
    naver_tfidf_lr = joblib.load('static/model/naver_tfidf_lr.pkl')
    naver_tfidf_nb = joblib.load('static/model/naver_tfidf_nb.pkl')
    ''' news_count_lr = joblib.load('static/model/news_count_lr.pkl')
    news_tfidf_lr = joblib.load('static/model/news_tfidf_lr.pkl')
    news_tfidf_sv = joblib.load('static/model/news_tfidf_sv.pkl') '''

@aclsf_bp.route('/digits', methods=['GET', 'POST'])
def digits():
    if request.method == 'GET':
        return render_template('advanced/digits.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        index_list = list(range(index, index+5))
        digits = load_digits()
        df = pd.read_csv('static/data/digits_test.csv')
        img_index_list = df['index'].values
        target_index_list = df['target'].values
        index_list = img_index_list[index:index+5]

        scaler = joblib.load('static/model/digits_scaler.pkl')
        test_data = df.iloc[index:index+5, 1:-1]
        test_scaled = scaler.transform(test_data)
        label_list = target_index_list[index:index+5]
        lrc = joblib.load('static/model/digits_lr.pkl')
        svc = joblib.load('static/model/digits_sv.pkl')
        rfc = joblib.load('static/model/digits_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/digit')
        for k, i in enumerate(index_list):
            plt.figure(figsize=(2,2))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(k+1) + '.png'
            plt.imshow(digits.images[i], cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list,
                       'pred_lr':pred_lr, 'pred_sv':pred_sv, 'pred_rf':pred_rf}
        
        return render_template('advanced/digits_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@aclsf_bp.route('/mnist', methods=['GET', 'POST'])
def mnist():
    if request.method == 'GET':
        return render_template('advanced/mnist.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        index_list = list(range(index, index+3))
        df = pd.read_csv('static/data/mnist/mnist_test.csv')

        scaler = joblib.load('static/model/mnist_scaler.pkl')
        test_data = df.iloc[index:index+3, :-1].values
        test_scaled = scaler.transform(test_data)
        label_list = df.iloc[index:index+3, -1]
        svc = joblib.load('static/model/mnist_sv.pkl')
        pred_sv = svc.predict(test_scaled)

        img_file_wo_ext = os.path.join(current_app.root_path, 'static/img/mnist')
        for i in range(3):
            digit = test_data[i].reshape(28,28)
            plt.figure(figsize=(4,4))
            plt.xticks([]); plt.yticks([])
            img_file = img_file_wo_ext + str(i+1) + '.png'
            plt.imshow(digit, cmap=plt.cm.binary, interpolation='nearest')
            plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index_list, 'label':label_list, 'pred_sv':pred_sv,}
        
        return render_template('advanced/mnist_res.html', menu=menu, mtime=mtime,
                                result=result_dict, weather=get_weather())

@aclsf_bp.route('/imdb', methods=['GET', 'POST'])
def imdb():
    if request.method == 'GET':
        return render_template('advanced/imdb.html', menu=menu, weather=get_weather())
    else:
        test_data = []
        if request.form['option'] == 'index':
            index = int(request.form['index'] or '0')
            df_test = pd.read_csv('static/data/IMDB_test.csv')
            test_data.append(df_test.iloc[index, 0])
            label = '긍정' if df_test.sentiment[index] else '부정'
        else:
            test_data.append(request.form['review'])
            label = '직접 확인'

        imdb_count_lr = joblib.load('static/model/imdb_count_lr.pkl')
        imdb_tfidf_lr = joblib.load('static/model/imdb_tfidf_lr.pkl')
        pred_cl = '긍정' if imdb_count_lr.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if imdb_tfidf_lr.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_tl':pred_tl}
        return render_template('advanced/imdb_res.html', menu=menu, review=test_data[0],
                                res=result_dict, weather=get_weather())

@aclsf_bp.route('/naver', methods=['GET', 'POST'])
def naver():
    if request.method == 'GET':
        return render_template('advanced/naver.html', menu=menu, weather=get_weather())
    else:
        if request.form['option'] == 'index':
            index = int(request.form['index'] or '0')
            df_test = pd.read_csv('static/data/naver/movie_test.tsv', sep='\t')
            org_review = df_test.document[index]
            label = '긍정' if df_test.label[index] else '부정'
        else:
            org_review = request.form['review']
            label = '직접 확인'
 
        test_data = []
        review = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", org_review)
        okt = Okt()
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다','을']
        morphs = okt.morphs(review, stem=True) # 토큰화
        temp_X = ' '.join([word for word in morphs if not word in stopwords]) # 불용어 제거
        test_data.append(temp_X)

        ''' naver_count_lr = joblib.load('static/model/naver_count_lr.pkl')
        naver_count_nb = joblib.load('static/model/naver_count_nb.pkl')
        naver_tfidf_lr = joblib.load('static/model/naver_tfidf_lr.pkl')
        naver_tfidf_nb = joblib.load('static/model/naver_tfidf_nb.pkl') '''
        pred_cl = '긍정' if naver_count_lr.predict(test_data)[0] else '부정'
        pred_cn = '긍정' if naver_count_nb.predict(test_data)[0] else '부정'
        pred_tl = '긍정' if naver_tfidf_lr.predict(test_data)[0] else '부정'
        pred_tn = '긍정' if naver_tfidf_nb.predict(test_data)[0] else '부정'
        result_dict = {'label':label, 'pred_cl':pred_cl, 'pred_cn':pred_cn,
                                      'pred_tl':pred_tl, 'pred_tn':pred_tn}
        return render_template('advanced/naver_res.html', menu=menu, review=org_review,
                                res=result_dict, weather=get_weather())

@aclsf_bp.route('/news', methods=['GET', 'POST'])
def news():
    target_names = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc',
                    'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',
                    'misc.forsale', 'rec.autos', 'rec.motorcycles', 'rec.sport.baseball',
                    'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
                    'sci.space', 'soc.religion.christian', 'talk.politics.guns',
                    'talk.politics.mideast', 'talk.politics.misc', 'talk.religion.misc']
    if request.method == 'GET':
        return render_template('advanced/news.html', menu=menu, weather=get_weather())
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/news/test.csv')
        label = f'{df.target[index]} ({target_names[df.target[index]]})'
        test_data = []
        test_data.append(df.data[index])

        news_count_lr = joblib.load('static/model/news_count_lr.pkl')
        news_tfidf_lr = joblib.load('static/model/news_tfidf_lr.pkl')
        news_tfidf_sv = joblib.load('static/model/news_tfidf_sv.pkl')
        pred_c_lr = news_count_lr.predict(test_data)
        pred_t_lr = news_tfidf_lr.predict(test_data)
        pred_t_sv = news_tfidf_sv.predict(test_data)
        result_dict = {'index':index, 'label':label, 
                       'pred_c_lr':f'{pred_c_lr[0]} ({target_names[pred_c_lr[0]]})',
                       'pred_t_lr':f'{pred_t_lr[0]} ({target_names[pred_t_lr[0]]})',
                       'pred_t_sv':f'{pred_t_sv[0]} ({target_names[pred_t_sv[0]]})'}
        
        return render_template('advanced/news_res.html', menu=menu, news=df.data[index],
                                res=result_dict, weather=get_weather())


