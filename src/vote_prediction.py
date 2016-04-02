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

if __name__ == "__main__":
	state = "NH"
	frontrunnerList = ["Clinton", "Cruz", "Sanders", "Trump"]
	counties = ["Belknap", "Carroll", "Cheshire", "Coos", "Grafton", "Hillsborough", "Merrimack", "Rockingham", "Strafford", "Sullivan", "Other", "Total"]
	candidates = ["Bush", "Carson", "Christie", "Clinton", "Cruz", "Gilmore", "Graham", "Huckabee", "Jindal", "Kasich", "Lessig", "O'Malley", "Paul", "Rubio", "Sanders", "Santorum", "Trump"]

	# change "NH_Results.csv" & "NH_Tweets.csv" to your file names
	csv.writer(file('train.tsv', 'w+'), delimiter='\t').writerows(csv.reader(open('NH_Results.csv', 'rU')))
	csv.writer(file('test.tsv', 'w+'), delimiter='\t').writerows(csv.reader(open('NH_Tweets.csv', 'rU')))

	# converting csv files to tsv files
	print "Checking & fixing voter tweets file & outputting to tsv file..."
	train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'train.tsv'), index_col=0, header=0, delimiter="\t", quoting=3, error_bad_lines=False)
	print "Checking & fixing election results file & outputting to tsv file..."
	test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'test.tsv'), index_col=0, header=0, delimiter="\t", quoting=3, error_bad_lines=False)
	print "Done.\n"

	# compare (rows, columns)
	# note: row/column amounts should match
	print "Comparing the following shapes:"
	print "Test (tweet data):", test.shape
	print "Train (election data):", train.shape, "\n"

	# quick test to make sure our frontrunners' tweets are being read-in correctly
	# note: to pull tweets, the format is test[column][row] or train[column][row]
	for frontrunner in frontrunnerList:
		print "Total # of votes in", state, "for", frontrunner, ":", train["Total"][frontrunner]
		print "Tweet(s) about", frontrunner, "in Belknap:", test["Belknap"][frontrunner], "\n"

	# here is a list of all tweets
	tweetList = []
	for candidate in candidates:
		for county in counties:
			tweetList.append(test[county][candidate])

	# here is a dictionary of tweets/candidate (not currently used, but may be used later)
	# puts each candidates' tweets into tweetList_"candidate" i.e. tweetList_Bush
	dct = defaultdict(list)
	for candidate in candidates:
		for county in counties:
			dct['tweetList_%s' % candidate].append(test[county][candidate])

	# testing a candidates' tweetList (gilmore is useful because he doesn't have many)
	#print "Gilmore's tweets:", (dct['tweetList_Gilmore'])

	# download nltk sets if you haven't already, otherwise comment this out
	nltk.download()
	
	# cleaning up tweetList
	# need to get BeautifulSoup working
	# need to get re.sub() replacement working so we can remove punctuation
	# check kaggle pt. 1 for instructions on both
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

	# looking at this, we can see that stopwords is working
	# but text is still pretty messy w/o beautifulsoup or re.sub()
	# an alternative option is to use CountVectorizer to clean up text
	# note: print statement is commented out because it's lengthy
	length = len(cleanTweetList)
	#for i in range (0, length):
	#	print cleanTweetList[i]

	vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
	testData = vectorizer.fit_transform(cleanTweetList)
	testDataArray = testData.toarray()

	# verify that vocabulary found looks correct
	# note: print commented out because it's lengthy
	vocab = vectorizer.get_feature_names()
	#print vocab

	# prints counts of each word in vocab (super interesting)
	# note: print commented out because it's lengthy
	dist = np.sum(testDataArray, axis=0)
	#for tag, count in zip(vocab, dist):
	#	print count, tag

	# compare (rows, features)
	# note: row numbers must match for shape comparison to work
	print "Comparing the following shapes:"
	print testDataArray.shape
	print test["Total"].shape, "\n"

	# use sklearn SVR .fit(x, y) to analyze
	# x: testDataArray, y: prediction
	regressor = SVR()
	regressor = regressor.fit(testDataArray, test["Total"])

	print "Making predictions..."

	# use sklearn SVR to make predictions
	results = regressor.predict(testDataArray)

	print "Outputting results to file..."

	# guesses don't appear to be correct (they're too close to carson's # of votes)
	# who wants to help point out my errors?
	output = pd.DataFrame(data={"Candidate":candidates, "Estimated Votes":results, "Actual Votes":test["Total"]})
	output.to_csv("NH_Guess.csv", delimiter=",", index=False, quoting=csv.QUOTE_MINIMAL, error_bad_lines=False)

	print "Done.\n"

	# loading in pretrained word2vec twitter model
	# download "twitter (2B Tweets)" with 25 dimensions from the following link
  	# https://github.com/3Top/word2vec-api
  	# then unzip the folder into the same folder as machine_learning.py
	# the section is commented out because it throws errors currently
	# note: need to delete our candidate's names from model (if they're even in there)
  	#twitterModel = gensim.models.word2vec.Word2Vec.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'glove.twitter.27B.25d.txt'), binary=False)
