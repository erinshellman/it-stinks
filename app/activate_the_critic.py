import os
import yaml
import twitter
from ipdb import set_trace
import nltk
import collections
from twitter_api import TwitterApi
from sentiment_classifier import SentimentClassifier  
from flask import Flask
from flask import request 
from flask import render_template 
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'blah'

@app.route('/')
def the_critic():
  return render_template('index.html')

@app.route('/', methods = ['POST'])
def the_critic_post():

  twitter_api = TwitterApi()
  classifier = SentimentClassifier()

  # Get the query from the page input
  query = request.form['text']

  # TODO: if the query doesn't start with a hashtag, then add one
  
  tweets = twitter_api.search_tweets(query, 5)

  # Does it stink?
  jays_rating = classifier.run(tweets)

  return render_template("index.html", tweets = tweets, sentiment = jays_rating)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/how_it_works')
def how_it_works():
  return render_template('how_it_works.html')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host = '0.0.0.0', port = port, debug = True)
