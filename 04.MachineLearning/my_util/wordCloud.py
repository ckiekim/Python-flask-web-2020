import numpy as np 
import pandas as pd 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import nltk, re
from konlpy.tag import Okt

def engCloud(text, stop_words, mask_file, img_file, max_words=1000):
    stopwords = set(STOPWORDS)
    for sw in stop_words:
        stopwords.add(sw)

    if mask_file == None:
        wc = WordCloud(background_color='black', width=800, height=800, max_words=max_words, stopwords=stopwords)
    else:
        mask = np.array(Image.open(mask_file))
        wc = WordCloud(background_color='white', width=800, height=800, max_words=max_words, mask=mask, stopwords=stopwords)
    wc = wc.generate(text)
    plt.figure(figsize=(8,8), dpi=100)
    ax = plt.axes([0,0,1,1])
    #plt.imshow(wc, interpolation='bilinear')
    plt.imshow(wc, interpolation='nearest', aspect='equal')
    plt.axis('off')
    plt.savefig(img_file)

def hanCloud(text, stop_words, mask_file, img_file, max_words=1000):
    mpl.rc('font', family='Malgun Gothic')
    mpl.rc('axes', unicode_minus=False)
    okt = Okt()
    tokens = okt.nouns(text)
    new_text = []
    for token in tokens:
        text = re.sub('[a-zA-Z0-9]', '', token)
        new_text.append(text)
    new_text = [word for word in new_text if word not in stop_words]
    han_text = nltk.Text(new_text, name='한글 텍스트')
    data = han_text.vocab().most_common(300)
    if mask_file == None:
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf',
                        width=800, height=800,
                        relative_scaling = 0.2, background_color='black',
                        ).generate_from_frequencies(dict(data))
    else:
        mask = np.array(Image.open(mask_file))
        wc = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf',
                        width=800, height=800,
                        relative_scaling = 0.2, mask=mask,
                        background_color='white',
                        ).generate_from_frequencies(dict(data))

    plt.figure(figsize=(8,8), dpi=100)
    ax = plt.axes([0,0,1,1])
    #plt.imshow(wc, interpolation='bilinear')
    plt.imshow(wc, interpolation='nearest', aspect='equal')
    plt.axis('off')
    plt.savefig(img_file)