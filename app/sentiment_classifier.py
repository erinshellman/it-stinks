#!/usr/bin/env python

# TODO: Get a better input corpus
# TODO: Add some basic tweet clean-up to remove symbols and shit.

import yaml
import twitter
from ipdb import set_trace
import nltk
import collections

class SentimentClassifier:

  def __init__(self):
    self.training_tweets = [('I love this car', 'positive'),
                            ('This view is amazing', 'positive'),
                            ('I feel great this morning', 'positive'),
                            ('I am so excited about the concert', 'positive'),
                            ('He is my best friend', 'positive'),
                            ('I do not like this car', 'negative'),
                            ('This view is horrible', 'negative'),
                            ('I feel tired this morning', 'negative'),
                            ('I am not looking forward to the concert', 'negative'),
                            ('He is my enemy', 'negative')]

  def run(self, tweets):
    classifier = self.initialize_training_set()
    answer = self.does_it_stink(tweets, classifier)
    return answer

  def get_tweet_words(self, tweets):
    all_words = []
    for (words, sentiment) in tweets:
      print words, sentiment
      all_words.extend(words)
    return all_words

  def extract_features(self, document):
    word_features = self.get_word_features(document)
    document_words = set(document)
    features = {}
    for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
    return features

  def get_word_features(self, wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

  def initialize_training_set(self):
    training_word_sets = []
    for (words, sentiment) in self.training_tweets:
      # Remove words of size 1 or 2.
      filtered_words = [x.lower() for x in words.split() if len(x) >= 3]
      training_word_sets.append((filtered_words, sentiment))
    # Construct the training set
    training_set = nltk.classify.apply_features(self.extract_features, training_word_sets)

    # Create the classifier
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier

  def does_it_stink(self, tweets, classifier):
    votes = []
    for tweet in tweets:
      current_vote = classifier.classify(self.extract_features(tweet.split()))
      votes.append(current_vote)
    # Make decision
    tallied_votes = collections.Counter(votes)
    print tallied_votes
    # Jay Sherman breaks ties by biasing towards bad reviews.
    if tallied_votes['negative'] >= tallied_votes['positive']:
      return "It stinks!"
    else:
      return "It's ok."
