from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR
from sklearn import cross_validation
from gensim.models import Word2Vec
from vectorizer import vectorize
import pandas as pd
import gensim, csv, string, re, os

def main():
	candidates = ["Bush", "Carson", "Christie", "Clinton", "Cruz", "Gilmore", "Graham", "Huckabee", "Jindal", "Kasich", "Lessig", "O'Malley", "Paul", "Rubio", "Sanders", "Santorum", "Trump"]

	data = pd.read_csv('NH_Training.csv')
	train, test = cross_validation.train_test_split(data, test_size = 0.1)
	attributes_to_use = ['Tweet list']

	testDataArray = vectorize()
	print(testDataArray)
	# use sklearn SVR .fit(x, y) to analyze
	# x: testDataArray, y: prediction
	regressor = SVR()
	regressor = regressor.fit(testDataArray, test['Total'])

	print("Making predictions...")

	# use sklearn SVR to make predictions
	results = regressor.predict(testDataArray)

	print("Outputting results to a file...")

	output = pd.DataFrame(data={"Candidate":candidates, "Estimated Votes":results, "Actual Votes":test["Total"]})
	output.to_csv("NH_Guess.csv", delimiter=",", index=False, quoting=csv.QUOTE_MINIMAL, error_bad_lines=False)

	print("Done.\n")

def pretrainedTwitterVectors():
	# loading in pretrained word2vec twitter model
	# download "twitter (2B Tweets)" with 25 dimensions from the following link
  	# https://github.com/3Top/word2vec-api
  	# then unzip the folder into the same folder as machine_learning.py
	# the section is commented out because it throws errors currently
	# note: need to delete our candidate's names from model (if they're even in there)
  	twitterModel = gensim.models.word2vec.Word2Vec.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'glove.twitter.27B.25d.txt'), binary=False)

  	return twitterModel

main()
