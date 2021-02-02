from flask import Blueprint, render_template, request, session, g
from flask import current_app
from werkzeug.utils import secure_filename
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import os
import pandas as pd
import matplotlib.pyplot as plt 
from my_util.weather import get_weather

clus_bp = Blueprint('clus_bp', __name__)

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

@clus_bp.route('/cluster', methods=['GET', 'POST'])
def cluster():
    menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':1, 'nl':0}
    if request.method == 'GET':
        return render_template('cluster/cluster.html', menu=menu, weather=get_weather_main())
    else:
        k_number = int(request.form['k_number'])
        f_csv = request.files['csv']
        file_csv = os.path.join(current_app.root_path, 'static/upload/') + f_csv.filename
        f_csv.save(file_csv)
        current_app.logger.debug(f"{k_number}, {f_csv}, {file_csv}")

        df_csv = pd.read_csv(file_csv)
        # 전처리 - 정규화
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_csv.iloc[:, :-1])

        # 차원 축소(PCA)
        pca = PCA(n_components=2)
        pca_array = pca.fit_transform(X_scaled)
        df = pd.DataFrame(pca_array, columns=['pca_x', 'pca_y'])
        df['target'] = df_csv.iloc[:, -1].values

        # K-Means Clustering
        kmeans = KMeans(n_clusters=k_number, init='k-means++', max_iter=300, random_state=2021)
        kmeans.fit(X_scaled)
        df['cluster'] = kmeans.labels_

        # 시각화
        markers = ['s', 'o', '^', 'P', 'D', 'H', 'x']
        plt.figure()
        for i in df.target.unique():
            marker = markers[i]
            x_axis_data = df[df.target == i]['pca_x']
            y_axis_data = df[df.target == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data, marker=marker)
        plt.title('Original Data Visualization by 2 PCA Components')
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        img_file = os.path.join(current_app.root_path, 'static/img/cluster0.png')
        plt.savefig(img_file)

        plt.figure()
        for i in range(k_number):
            marker = markers[i]
            x_axis_data = df[df.cluster == i]['pca_x']
            y_axis_data = df[df.cluster == i]['pca_y']
            plt.scatter(x_axis_data, y_axis_data, marker=marker)
        plt.xlabel('PCA 1'); plt.ylabel('PCA 2')
        plt.title(f'{k_number} Clusters Visualization by 2 PCA Components')
        img_file = os.path.join(current_app.root_path, 'static/img/cluster1.png')
        plt.savefig(img_file)

        mtime = int(os.stat(img_file).st_mtime)
        return render_template('cluster/cluster_res.html', menu=menu, weather=get_weather_main(),
                                k_number=k_number, mtime=mtime)
