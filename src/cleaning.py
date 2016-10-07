from collections import defaultdict
from bs4 import BeautifulSoup
from array import array
from nltk.corpus import stopwords
from sklearn import cross_validation
import pandas as pd
import gensim, nltk, csv, string, re, os

# note: run 'easy_install -U gensim' in terminal before importing gensim

def main():
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

	data = pd.read_csv('NH_Training.csv')
	print(data)
	train, test = cross_validation.train_test_split(data, test_size = 0.1)
	attributes_to_use = ['Tweet list']

	print ("\nCleaning tweets...")

	cleanTweetList = []

	words = " ".join(map(str, data['Tweet list']))
	words = words.lower().split()
	stops = set(stopwords.words("english"))
	meaningfulWords = [w for w in words if not w in stops]
	cleanTweets = " ".join(meaningfulWords)
	cleanTweetList.append(cleanTweets)

	print("Done.\n")

	return cleanTweetList

main()