from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR
from gensim.models import Word2Vec
from collections import defaultdict
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from array import array
import pandas as pd
import numpy as np
import gensim, nltk, logging, csv, string, re, os

# note: run 'easy_install -U gensim' in terminal before importing gensim

def getTrainingList():
	csv.writer(open('train.tsv', 'w+'), delimiter='\t').writerows(csv.reader(open('NH_Results.csv', 'rU')))

	# converting csv files to tsv files
	train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'train.tsv'), index_col=0, header=0, delimiter="\t", quoting=3, error_bad_lines=False)
	return train

def getTestingList():
	csv.writer(open('test.tsv', 'w+'), delimiter='\t').writerows(csv.reader(open('NH_Tweets.csv', 'rU')))

	# converting csv files to tsv files
	test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test.tsv'), index_col=0, header=0, delimiter="\t", quoting=3, error_bad_lines=False)
	return test

def compareShapes(test_list, train_list):
	# compare (rows, columns)
	print("Comparing the following shapes:")
	print("Test (tweet data):", test_list.shape)
	print("Train (election data):", train_list.shape, "\n")

def tweetVerification(frontrunner_list):
	# quick test to make sure our frontrunners' tweets are being read-in correctly
	# note: to pull tweets, the format is test[column][row] or train[column][row]
	for frontrunner in frontrunner_list:
		print("Total # of votes in", state, "for", frontrunner, ":", train["Total"][frontrunner])
		print("Tweet(s) about", frontrunner, "in Belknap:", test["Belknap"][frontrunner], "\n")

def tweetList(candidate_list, county_list):
	# here is a list of all tweets
	tweetList = []
	for candidate in candidate_list:
		for county in county_list:
			tweetList.append(test[county][candidate])

def tweetDictionary(candidate_list, county_list):
	# here is a dictionary of tweets/candidate (not currently used, but may be used later)
	# puts each candidates' tweets into tweetList_"candidate" i.e. tweetList_Bush
	dct = defaultdict(list)
	for candidate in candidate_list:
		for county in county_list:
			dct['tweetList_%s' % candidate].append(test[county][candidate])

	# testing a candidates' tweetList (gilmore is useful because he doesn't have many)
	print("Gilmore's tweets:", (dct['tweetList_Gilmore']))
	
def cleanTweets():
	# cleaning up tweetList
	# TODO: get BeautifulSoup working
	# TODO: get re.sub() replacement working so we can remove punctuation
	# check kaggle pt. 1 for instructions on both

	# download nltk sets if you haven't already, otherwise comment this out
	#nltk.download()

	state = "NH"
	frontrunnerList = ["Clinton", "Cruz", "Sanders", "Trump"]
	counties = ["Belknap", "Carroll", "Cheshire", "Coos", "Grafton", "Hillsborough", "Merrimack", "Rockingham", "Strafford", "Sullivan", "Other", "Total"]
	candidates = ["Bush", "Carson", "Christie", "Clinton", "Cruz", "Gilmore", "Graham", "Huckabee", "Jindal", "Kasich", "Lessig", "O'Malley", "Paul", "Rubio", "Sanders", "Santorum", "Trump"]

	test = getTestingList()

	print ("\nCleaning tweets...")

	candidateTweets = []
	cleanTweetList = []
	for candidate in candidates:
		for county in counties:
			text = test[county][candidate]
			candidateTweets.append(text)
		words = " ".join(map(str, candidateTweets))
		words = words.lower().split()
		stops = set(stopwords.words("english"))
		meaningfulWords = [w for w in words if not w in stops]
		cleanTweets = " ".join(meaningfulWords)
		cleanTweetList.append(cleanTweets)

	print("Done.\n")

	return cleanTweetList

def viewCleanTweets(cleaned_tweet_list):
	# looking at this, we can see that stopwords is working
	# but text is still pretty messy w/o beautifulsoup or re.sub()
	# an alternative option is to use CountVectorizer to clean up text
	length = len(cleanTweetList)
	for i in range(0, length):
		print(cleanTweetList[i])