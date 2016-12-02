from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

def vectorize(data):    
    vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None, max_features=5000)
    vectorized_data = vectorizer.fit_transform(data['Tweet List'])
    vectorized_data = vectorized_data.toarray()
    vocab = vectorizer.get_feature_names()
    
    # view vocab
    #print(vocab)
    
    # view vocab count
    dist = np.sum(vectorized_data, axis = 0)
    #for tag, count in zip(vocab, dist):
        #print(count, tag)
    
    vector_dataframe = pd.DataFrame(vectorized_data)
    
    x = 0
    while x < len(vocab):
        vector_dataframe.rename( columns = {x: vocab[x]}, inplace = True )
        x = x + 1
    
    new_dataframe = pd.concat([data, vector_dataframe], axis=1)
    #new_dataframe.to_csv("full_dataframe.csv")
    
    return new_dataframe

#candidate_data = clean()
#vectorized_data = vectorize(candidate_data)
