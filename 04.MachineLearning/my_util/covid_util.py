import requests
from bs4 import BeautifulSoup
from flask import current_app
import pandas as pd
import db.db_module as dm

def change_date(x):
    y = x.split(' ')
    month = y[1][:-1] if len(y[1][:-1]) == 2 else '0'+y[1][:-1]
    day = y[2][:-1] if len(y[2][:-1]) == 2 else '0'+y[2][:-1]
    return f'{y[0][:-1]}-{month}-{day}'

def get_region_by_date(date):
    with open('static/data/gov_data_api_key.txt', mode='r') as key_fd:
        govapi_key = key_fd.read(100)
    start_date = date.replace('-','')
    end_date = date.replace('-','')
    page = 1
    corona_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    url = f'{corona_url}?ServiceKey={govapi_key}&pageNo={page}&numOfRows=10&startCreateDt={start_date}&endCreateDt={end_date}'

    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')
    resultCode = soup.find('resultCode').get_text()
    if resultCode == '99':
        current_app.logger.info(soup.find('resultMsg').string)
        return
    if resultCode == '00' and soup.find('totalCount').string == '0':
        current_app.logger.info('There is no data!!!')
        return

    items = soup.find_all('item')
    item_count = len(items)
    print(item_count)
    for index, item in enumerate(items):
        if item_count > 30 and index >= int(item_count/2):
            break
        stdDay = change_date(item.find('stdDay').string)
        deathCnt = int(item.find('deathCnt').string) if item.find('deathCnt') else 0
        defCnt = int(item.find('defCnt').string) if item.find('defCnt') else 0
        gubun = item.find('gubun').string
        incDec = int(item.find('incDec').string)
        isolClearCnt = int(item.find('isolClearCnt').string) if item.find('isolClearCnt') else 0
        isolIngCnt = int(item.find('isolIngCnt').string) if item.find('isolIngCnt') else 0
        localOccCnt = int(item.find('localOccCnt').string) if item.find('localOccCnt') else 0
        overFlowCnt = int(item.find('overFlowCnt').string) if item.find('overFlowCnt') else 0
        qurRate = None
        if item.find('qurRate'):
            qur = item.find('qurRate').string
            if qur != None and qur.count('.') == 2:
                qur = qur[:-1]
            #print(qur)
            if qur != None and qur[0] in '0123456789':
                qurRate = float(qur)
    
        params = [stdDay, deathCnt, defCnt, gubun, incDec, isolClearCnt, isolIngCnt, 
                localOccCnt, overFlowCnt, qurRate]
        dm.write_region(params)
    
    current_app.logger.info(f'{date} region data successfully inserted.')

def get_agender_by_date(date):
    with open('static/data/gov_data_api_key.txt', mode='r') as key_fd:
        govapi_key = key_fd.read(100)
    start_date = date.replace('-','')
    end_date = date.replace('-','')
    page = 1
    corona_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson'
    url = f'{corona_url}?ServiceKey={govapi_key}&pageNo={page}&numOfRows=10&startCreateDt={start_date}&endCreateDt={end_date}'

    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')
    resultCode = soup.find('resultCode').get_text()
    if resultCode == '99':
        current_app.logger.info(soup.find('resultMsg').string)
        return
    if resultCode == '00' and soup.find('totalCount').string == '0':
        current_app.logger.info('There is no data!!!')
        return
        
    items = soup.find_all('item')
    for item in items:
        createDt = item.find('createDt').string.split(' ')[0]
        confCase = int(item.find('confCase').string)
        confCaseRate = float(item.find('confCaseRate').string)
        death = int(item.find('death').string)
        deathRate = float(item.find('deathRate').string)
        criticalRate = float(item.find('criticalRate').string)
        gubun = item.find('gubun').string
        seq = int(item.find('seq').string)
        updateDt = item.find('updateDt').string

        params = [createDt, confCase, confCaseRate, death, deathRate, criticalRate,
                    gubun,seq,updateDt]
        dm.write_agender(params)

    current_app.logger.info(f'{date} agender data successfully inserted.')

def get_daily(df, col, new):
    diff = [0]
    for i in range(1, len(df)):
        diff.append(df[col][i] - df[col][i-1])
    del df[col]
    df[new] = diff
    return df

def make_corona_raw_df(start_date, end_date):
    c_rows = []
    items = 'sid, confDay, region, status'
    gu_list = ['강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구',
               '노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구','성동구',
               '성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구']
    for gu in gu_list:
        rows = dm.get_seoul_items_by_condition(items, gu, start_date, end_date)
        c_rows.extend(rows)
    df = pd.DataFrame(c_rows, columns=['sid', '확진일', 'gu', 'status'])
    df['확진일'] = pd.to_datetime(df['확진일'])
    cdf_raw = pd.pivot_table(df, values='sid', index='확진일', columns='gu', aggfunc='count')
    cdf_raw.fillna(0, inplace=True)
    cdf_raw = cdf_raw.astype(int)
    cdf_raw['합계'] = cdf_raw.sum(axis=1)
    return cdf_raw, gu_list

def make_corona_df(cdf_raw):
    cdfM = cdf_raw.resample('M').sum().astype(int)
    cdfM.index = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월']
    cdf = cdfM.T
    cdf['누적'] = cdf.sum(axis=1)

    pop = pd.read_csv('./static/data/cctv.csv')     # 구별 인구 데이터 참조
    pop.set_index('구별', inplace=True)
    cdf['인구수'] = pop['인구수']
    cdf['천명당 확진자 수'] = cdf['누적'] / cdf['인구수'] * 1000
    return cdf.iloc[:-1, :]     # 마지막 합계 행은 제거

def get_new_seoul_data():
    with open('static/data/seoul_api_key.txt', mode='r') as key_fd:
        seoulapi_key = key_fd.read(100)
    corona_url = 'http://openapi.seoul.go.kr:8088'
    type = 'xml'
    url = f'{corona_url}/{seoulapi_key}/{type}/Corona19Status/1/10'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')
    resultCode = soup.find('RESULT').find('CODE').get_text()
    if resultCode == 'INFO-000':
        list_total_count = int(soup.find('list_total_count').get_text())
        current_app.logger.debug(list_total_count)
    else:
        current_app.logger.info(soup.find('RESULT').find('MESSAGE').get_text())
        return

    last_sid = dm.get_seoul_last_sid()
    if list_total_count <= last_sid:
        return
    read_count = list_total_count - last_sid

    id_list, date_list, area_list, travel_list = [],[],[],[]
    contact_list, status_list, moving_list = [],[],[]

    for i in range(1, read_count, 1000):
        start_index = i
        end_index = i+1000-1 if i+1000-1<read_count else read_count
        url = f'{corona_url}/{seoulapi_key}/{type}/Corona19Status/{start_index}/{end_index}'
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'xml')
        items = soup.find_all('row')

        for item in items:
            id_list.append(item.find('CORONA19_ID').string)
            date_list.append(item.find('CORONA19_DATE').string)
            area_list.append(item.find('CORONA19_AREA').string)
            travel_list.append(item.find('CORONA19_TRAVEL_HISTORY').string)
            contact_list.append(item.find('CORONA19_CONTACT_HISTORY').string)
            status_list.append(item.find('CORONA19_LEAVE_STATUS').string)
            moving_list.append(item.find('CORONA19_MOVING_PATH').string)

    df = pd.DataFrame({
        '연번':id_list, '확진일':date_list, '지역':area_list, '여행력':travel_list,
        '접촉력':contact_list, '상태':status_list, '이동경로':moving_list
    })
    df['연번'] = df['연번'].astype(int)
    df.sort_values('연번', inplace=True)
    #df['확진일'] = pd.to_datetime('2020.'+df['확진일']).astype(str)
    df['확진일'] = pd.to_datetime(df['확진일']).astype(str)
    df['지역'].fillna('기타', inplace=True)
    df['지역'] = df['지역'].map(lambda s: s.strip())
    df.fillna(' ', inplace=True)

    dm.insert_seoul_bulk_data(df)
    ''' for i in df.index:
        params = [int(df.iloc[i,0])]
        params.extend(df.iloc[i,1:])
        dm.insert_seoul_data(params) '''