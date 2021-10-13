# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 09:55:00 2021

@author: wyang
"""
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

articles_org = pd.read_csv('https://raw.githubusercontent.com/wyang23/architectgooddata/main/gooddata.csv', encoding = 'ISO-8859-1')

#articles_org = pd.read_csv(url)
print(articles_org.head(3))
articles = articles_org[[ 'Author', 'Title','Keywords']]
articles['combined_features'] = articles['Author'] +' '+ articles['Title'] +' '+ articles['Keywords']

articles.iloc[0]['combined_features']

cv = CountVectorizer()
count_matrix = cv.fit_transform(articles['combined_features'])
cs = cosine_similarity(count_matrix)
cs.shape

def get_article_title_from_index(index):
    return articles_org[articles_org['Index']==index]['Title'].values[0]
def get_index_from_article_title(name):
    return articles_org[articles_org['Title']==name]['Index'].values[0]

#@app.route('/')
#def hello_world():
#    return "Hello world"

@app.route('/api', methods = ['GET'])
def getRecommendations():

    inputchr = str(request.args['query'])
    print(request.args['query'])
    print(inputchr)
    #test_article_title = input('Enter Article name --> ')
    test_article_title = inputchr
    test_article_index = get_index_from_article_title(test_article_title)
    articles_corrs = cs[test_article_index]
    articles_corrs = enumerate(articles_corrs)
    sorted_similar_articles = sorted(articles_corrs,key=lambda x:x[1],reverse=True)
    return get_article_title_from_index(sorted_similar_articles[1][0])
    

#getRecommendations(title="The challenge of opening up gated communities in Shanghai")
#title = "yes"

if __name__ == '__main__':
    #getRecommendations(title="The challenge of opening up gated communities in Shanghai")
    app.run(host='0.0.0.0')
    #app.run(host='0.0.0.0', port='8080', debug=True)
