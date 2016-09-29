from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR
from gensim.models import Word2Vec
from collections import defaultdict
from nltk.corpus import stopwords
from cleaning import cleanTweets
from bs4 import BeautifulSoup
from array import array
import pandas as pd
import numpy as np
import gensim, nltk, logging, csv, string, re, os

def vectorize():
	cleanTweetList = cleanTweets()

	print("Vectorizing...")

	vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
	testData = vectorizer.fit_transform(cleanTweetList)
	testDataArray = testData.toarray()
	print("Done.\n")
	return testDataArray

def verifyVocab():
	# verify that vocabulary found looks correct
	vocab = vectorizer.get_feature_names()
	print(vocab)

def vocabCounts():
	# counts of each word in vocab (super interesting)
	dist = np.sum(testDataArray, axis=0)
	for tag, count in zip(vocab, dist):
		print(count, tag)