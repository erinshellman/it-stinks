#!/usr/bin/env python

import yaml
import twitter
from ipdb import set_trace
import nltk
import collections

class TwitterApi:

  def __init__(self):
    self.auth = twitter.oauth.OAuth(
      OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    self.twitter_object = twitter.Twitter(auth = self.auth)

  def search_tweets(self, search_query, count):
    search_results = self.twitter_object.search.tweets(
          q = search_query, count = count)
    # returns only statuses
    statuses = search_results['statuses']

    text = list()
    for status in statuses:
      text.append(status['text'])
    return text 
