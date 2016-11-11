from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection as ms
from gensim.models import Word2Vec
from vectorizer import vectorize
from cleaning import clean
import pandas as pd

def prediction(vectorized_data):   
    headers = list(vectorized_data.columns.values)
    vector_headers = headers[5:]

    target_column = vectorized_data['Number of Votes']
    predictor_columns = vectorized_data.drop('Number of Votes', 1)
    vector_columns = vectorized_data[vector_headers]
    
    (train_data, test_data, train_target, test_target) =  ms.train_test_split(predictor_columns, target_column, test_size = 0.15)    
    
    classifier = RandomForestClassifier(n_estimators=10)
    classifier = classifier.fit(train_data[vector_headers], train_target)
    results = classifier.predict(test_data[vector_headers])
    
    output = pd.DataFrame(data={"Candidate":test_data['Candidate'], "County":test_data['County'], "Estimated Votes":results, "Actual Votes":test_target})    
    return output

cleaned_tweets = clean()
vectorized_data = vectorize(cleaned_tweets)
results = prediction(vectorized_data)
print(results)