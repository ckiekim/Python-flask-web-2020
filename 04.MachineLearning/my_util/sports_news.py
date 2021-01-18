import requests, time
from selenium import webdriver
from flask import current_app

def get_sports_news(filename):
    driver = webdriver.Chrome('./bp6_wordcloud/chromedriver')
    url = 'https://sports.news.naver.com/index.nhn'
    driver.get(url)
    time.sleep(1)

    menus = driver.find_elements_by_class_name('main_menu_item')
    events = []
    for i in range(1, len(menus)-4):
        event = menus[i].find_element_by_tag_name('a').get_attribute('href')
        events.append(event.split('/')[3])

    base_url = 'https://sports.news.naver.com/'
    option_url = '/news/index.nhn?isphoto=N&page='
    title_list = []
    for event in events:
        #print(event, end=': 1, ')
        current_app.logger.debug(f'{event} - 1')
        url = f'{base_url}{event}{option_url}{i}'
        driver.get(url)
        time.sleep(2)
        news = driver.find_element_by_css_selector('.news_list')
        ul = news.find_element_by_tag_name('ul')
        lis = ul.find_elements_by_tag_name('li')
        for li in lis:
            text = li.find_element_by_css_selector('.text')
            title = text.find_element_by_tag_name('span').text
            title_list.append(title)

        while True:
            page = driver.find_element_by_id('_pageList')
            try:
                next = page.find_element_by_class_name('next')
                if next:
                    next.click()
            except:
                break

        page = driver.find_element_by_id('_pageList')
        try:
            atags = page.find_elements_by_tag_name('a')
            numPage = int(atags[-1].text)
        except:
            numPage=1

        for i in range(2, numPage+1):
            #print(i, end=', ')
            current_app.logger.debug(f'{event} - {i}')
            url = f'{base_url}{event}{option_url}{i}'
            driver.get(url)
            time.sleep(2)
            news = driver.find_element_by_css_selector('.news_list')
            ul = news.find_element_by_tag_name('ul')
            lis = ul.find_elements_by_tag_name('li')
            for li in lis:
                text = li.find_element_by_css_selector('.text')
                title = text.find_element_by_tag_name('span').text
                title_list.append(title)
        #print()

    driver.close()
    title_str = ' '.join(title for title in title_list)
    file = open(filename, 'w', encoding='utf-8')
    file.write(title_str)
    file.close()
