# Library imports
import numpy as np
import sqlite3
import pickle
import os

from .vectorizer import vectorizer

# Define update function to update the classifier model
def update_model(db_path, model, batch_size = 10000):
    connection = sqlite3.connect(db_path, timeout = 10)             # Establish connection to review database
    c = connection.cursor()
    c.execute('Select * from review_db')

    results = c.fetchmany(batch_size)                               # Fetch up to 10000 movie reviews
    while results:
        data = np.array(results)
        X = data[:, 0]
        y = data[:, 1].astype(int)

        classes = np.array([0, 1])                                  # Train the model on the fetched movie reviews
        X_train = vectorizer.transform(X)
        model.partial_fit(X_train, y, classes = classes)
        results = c.fetchmany(batch_size)

    c.close()                                                       # Close connection to database
    return model

current_directory = os.path.dirname(__file__)
classifier = pickle.load(open(os.path.join(current_directory, 'pkl_objects', 'classifier.pkl'), 'rb'))

db = os.path.join(current_directory, 'reviews.sqlite')

classifier = update_model(db_path=db, model=classifier, batch_size=10000)

# Permanently update classifier.pkl file
pickle.dump(classifier, open(os.path.join(current_directory, 'pkl_objects', 'classifier.pkl'), 'wb'), protocol=4)