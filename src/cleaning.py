from collections import defaultdict
from nltk.corpus import stopwords
import pandas as pd
import re

def clean():
    # download nltk sets if you haven't already
    #nltk.download()

    # file to pull candidate, county, votes & tweets from
    candidate_data = pd.read_csv('NH_Data.csv')
    tweet_list = []
    
    candidate_data['Tweet list'] = candidate_data['Tweet list'].fillna('')
    
    x = 0
    word_list = []
    all_words_list = []
    stop_words = set(stopwords.words("english"))
    stop_words.add('n')
    
    while x < len(candidate_data['Tweet list']):
        words = re.sub('[^\w-]', ' ', candidate_data['Tweet list'][x])
        word_list = words.split()
        word_list = [w for w in word_list if not w in stop_words]
        a_big_string = ', '.join(word_list)
        candidate_data['Tweet list'][x] = a_big_string
        x = x + 1
    
    return candidate_data

#result = clean()