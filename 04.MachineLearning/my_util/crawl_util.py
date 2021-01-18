import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from flask import current_app
import pandas as pd

def siksin(place):
    url_base = 'https://www.siksinhot.com'
    url_sub = '/search?keywords=' + quote(place)
    url = url_base + url_sub
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    lis = soup.select_one('.listTy1').find('ul').find_all('li')

    rest_list = []
    for i in range(0, len(lis), 5):
        store = lis[i].select_one('.store').string
        img = lis[i].find('img').attrs['src'].split('?')[0]
        href = lis[i].find('a').attrs['href']
        url = url_base + href
        req = requests.get(url) 
        rest = BeautifulSoup(req.text, 'html.parser')
        feature = rest.select_one('.store_name_score').find('p').string
        tel = rest.select_one('.p_tel').find('p').get_text()
        addr = rest.select_one('.txt_adr').get_text()
        rest_list.append({'store':store, 'img':img, 'feature':feature,
                          'tel':tel, 'addr':addr, 'href':url})
    return rest_list

def genie():
    url = 'https://www.genie.co.kr/chart/top200'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get(url, headers = header)
    soup = BeautifulSoup(req.text, 'html.parser')
    trs = soup.select_one('.list-wrap').find('tbody').select('tr.list')

    music_list = []
    for index, tr in enumerate(trs):
        num = tr.select_one('.number').get_text()
        rank = f'<strong>{num.split()[0]}</strong>'
        last = num.split()[1]
        if last == '유지':
            rank += '<br><small>-</small>'
        elif last.find('상승') > 0:
            rank += f'<br><small><span style="color: red;">▲{last[:-2]}</span></small>'
        else:
            rank += f'<br><small><span style="color: blue;">▼{last[:-2]}</span></small>'
        title = tr.select_one('a.title').string.strip()
        artist = tr.select_one('a.artist').string
        album = tr.select_one('a.albumtitle').string
        img = 'https:' + tr.select_one('a.cover').find('img').attrs['src']
        music_list.append({'index':index, 'rank':rank, 'title':title, 'artist':artist,
                            'album':album, 'img':img})
    return music_list

def interpark():
    url_base = 'http://book.interpark.com'
    url_sub = '/display/collectlist.do?_method=bestsellerHourNew&bookblockname=b_gnb&booklinkname=%BA%A3%BD%BA%C6%AE%C1%B8&bid1=w_bgnb&bid2=LiveRanking&bid3=main&bid4=001'
    url = url_base + url_sub
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    lis = soup.select_one('.rankBestContentList ').select('.listItem.singleType')

    book_list = []
    for index, li in enumerate(lis):
        rank = index + 1
        title = li.select_one('.itemName').string.strip()
        author = li.select_one('.author').string
        company = li.select_one('.company').string
        price = li.select_one('.price').find('em').string
        href = url_base + li.select_one('.coverImage').find('a').attrs['href']
        img = li.select_one('.coverImage').find('img').attrs['src']
        book_list.append({'rank':rank, 'title':title, 'author':author,
                          'company':company, 'price':price, 'href':href, 'img':img})
    return book_list
