# Library imports
import pandas as pd
import numpy as np
import pickle
import nltk
import re
import os

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier

# Read the dataset into a dataframe
dataset_path = os.getcwd() + "\datasets\movie_data.csv"
movie_data = pd.read_csv(dataset_path)

# Download list of stopwords
nltk.download('stopwords')
stop = stopwords.words('english')

# Define tokenizer function to split text into individual elements, removing any stopwords
def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)

    text = (re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', ''))
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

# Define generator function that reads and returns one document at a time
def stream_docs(path):
    with open(path, 'r', encoding = 'utf-8') as csv:
        next(csv)

        for line in csv:
            text, label = line[:-3], int(line[-2])
            yield text, label

# Define batch function to take a document stream and return a number of documents
def get_minibatch(doc_stream, size):
    docs, y = [], []

    try:
        for _ in range(size):
            text, label = next(doc_stream)
            docs.append(text)
            y.append(label)
    except StopIteration:
        return None, None
    
    return docs, y

# # Create HashingVectorizer to create a 'bag-of-words' model, which converts text into numerical feature vectors
vectorizer = HashingVectorizer(decode_error = 'ignore', n_features = 2**21, preprocessor = None, tokenizer = tokenizer)
classifier = SGDClassifier(loss = 'log_loss', random_state = 1)
doc_stream = stream_docs(path = os.getcwd() + "\Datasets\movie_data.csv")

# Train the classifier model
classes = np.array([0, 1])

for _ in range(45):
    X_train, y_train = get_minibatch(doc_stream, size = 1000)
    if not X_train: break

    X_train = vectorizer.transform(X_train)
    classifier.partial_fit(X_train, y_train, classes = classes)

X_test, y_test = get_minibatch(doc_stream, size = 5000)
X_test = vectorizer.transform(X_test)
print("Accuracy: %.3f" % classifier.score(X_test, y_test))

classifier = classifier.partial_fit(X_test, y_test)

# Pickle the classifier model and stopwords
destination = os.path.join('movie_classifier', 'pkl_objects')
if not os.path.exists(destination): os.makedirs(destination)

pickle.dump(stop, open(os.path.join(destination, 'stopwords.pkl'), 'wb'), protocol = 4)
pickle.dump(classifier, open(os.path.join(destination, 'classifier.pkl'), 'wb'), protocol = 4)