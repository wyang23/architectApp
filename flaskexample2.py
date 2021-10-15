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

@app.route('/api', methods = ['GET'])
def getRecommendations():
    articleString = ""
    inputchr = str(request.args['query'])
    test_article_title = inputchr
    test_article_index = get_index_from_article_title(test_article_title)
    articles_corrs = cs[test_article_index]
    articles_corrs = enumerate(articles_corrs)
    sorted_similar_articles = sorted(articles_corrs,key=lambda x:x[1],reverse=True)
    for i in range(4):
            articleString += get_article_title_from_index(sorted_similar_articles[i+1][0])
            articleString += "^"
    return articleString[:-1]

@app.route('/api2', methods = ['GET'])
def getCombinedRecommendations():
    #titleList = titles.split("^")
    sumCosineScores = dict.fromkeys(range(83), 0)
    articleString = ""

    inputchr = str(request.args['query'])
    titleList = inputchr.split("^")

    for title in titleList:
        print(title)
        test_article_title = title
        test_article_index = get_index_from_article_title(test_article_title)
        articles_corrs = cs[test_article_index]
        articles_corrs = enumerate(articles_corrs)
        sorted_similar_articles = sorted(articles_corrs,key=lambda x:x[1],reverse=True)
        for i in range(83):
            sumCosineScores[sorted_similar_articles[i][0]] += sorted_similar_articles[i][1]
        print(sumCosineScores)
    
    for i in range(83):
        sumCosineScores[sorted_similar_articles[i][0]] = sumCosineScores[sorted_similar_articles[i][0]]/len(titleList)
    
    print(sumCosineScores)
    a = sorted(sumCosineScores.items(), key= lambda x:x[1], reverse = True)
    print(a)
    for i in range(8):
        print(get_article_title_from_index(a[i+len(titleList)][0]))
        articleString += get_article_title_from_index(a[i+len(titleList)][0])
        articleString += "^"
    print(articleString[:-1])
    return articleString[:-1]

if __name__ == '__main__':
    app.run(host='0.0.0.0')
