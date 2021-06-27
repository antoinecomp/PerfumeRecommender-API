import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Flask
from flaskext.mysql import MySQL
import config

import numpy as np

#instaniation
app = Flask(__name__)
app.secret_key= 'secret'

#config
app.config['MYSQL_DATABASE_USER'] = config.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_DATABASE_HOST

#init MySQL
mysql = MySQL()
mysql.init_app(app)

def get_data():
    # MySQL not working yet
    # #create Cursor
    # cur = mysql.get_db().cursor() #to execute commands
    # cur.execute("USE attributs")
    #
    # #get articles
    # result = cur.execute("SELECT * FROM attributs")
    # #should retrieve all as a dictionary
    # perfumes = cur.fetchall()
    perfumes_scores = pd.read_csv("https://raw.githubusercontent.com/antoinecomp/todowoo/main/data_management/attributes.csv")
    perfumes_scores = perfumes_scores.set_index('_id')
    perfumes_scores.columns = map(str.lower, perfumes_scores.columns)
    return perfumes_scores

def recommend_perfumes(perfumes_scores, features):
    # on prend uniquement les scores compris dans les features
    perfumes_scores = perfumes_scores[[features]]
    features_vector = pd.DataFrame(1, index=np.arange(len(perfumes_scores)), columns=[features])
    sim_scores = pd.DataFrame(perfumes_scores.values*features_vector.values,
                              columns=perfumes_scores.columns, index=perfumes_scores.index)
    sim_scores = sim_scores.sort_values(by=features, ascending=False)
    sim_scores = {"perfumes": [str(x) for x in sim_scores[0:5].index]}

    return sim_scores

def results(features):
    perfumes_scores = get_data()
    recommendations = recommend_perfumes(perfumes_scores, features)
    return recommendations