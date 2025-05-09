# Library imports
import pickle
import re
import os

from sklearn.feature_extraction.text import HashingVectorizer

# Load the list of stopwords
current_directory = os.path.dirname(__file__)
stop = pickle.load(open(os.path.join(current_directory, 'pkl_objects', 'stopwords.pkl'), 'rb'))


# Define tokenizer function to split text into individual elements, removing any stopwords
def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)

    text = (re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', ''))
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

# # Create HashingVectorizer to create a 'bag-of-words' model, which converts text into numerical feature vectors
vectorizer = HashingVectorizer(decode_error = 'ignore', n_features = 2**21, preprocessor = None, tokenizer = tokenizer)