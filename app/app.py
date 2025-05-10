# Library imports
import streamlit as st
import numpy as np
import sqlite3
import pickle
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from movie_classifier.vectorizer import vectorizer
from movie_classifier.update import update_model

# Load the classifier model
current_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'movie_classifier'))
classifier = pickle.load(open(os.path.join(current_directory, 'pkl_objects', 'classifier.pkl'), 'rb'))

# Get path to reviews database
db = os.path.join(current_directory, 'reviews.sqlite')

# Define classify function to perform prediction on given review
def classify(document):
    label = {0: 'negative', 1: 'positive'}
    X = vectorizer.transform([document])
    y = classifier.predict(X)[0]
    probabilty = np.max(classifier.predict_proba(X))

    return label[y], probabilty

# Define train function to train classifier on given review
def train(document, y):
    X = vectorizer.transform([document])
    classifier.partial_fit(X, [y])

# Define sqlite_entry function to add review and prediction to the movie reviews database
def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path, timeout = 10)
    c = conn.cursor()

    c.execute("INSERT INTO review_db (review, sentiment, date) VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

# Update the model before use using reviews from the database
classifier = update_model(db_path = db, model = classifier, batch_size = 10000)

st.set_page_config(
    page_title = 'Movie Review Sentiment Analysis'
)

if 'step' not in st.session_state: st.session_state.step = 'input'
if 'review' not in st.session_state: st.session_state.review = ""
if 'prediction' not in st.session_state: st.session_state.prediction = ""
if 'probability' not in st.session_state: st.session_state.probability = 0.0
if 'classified' not in st.session_state: st.session_state.classified = False
if 'feedback_submitted' not in st.session_state: st.session_state.feedback_submitted = False



title = st.title("Movie Review Sentiment Analysis")

if st.session_state.step == 'input':
    enter_review = st.header("Submit a Movie Review")
    review = st.text_area("Enter your review here: ")

    classify_button = st.button("Classify Review")
    if classify_button:
        if review.strip():
            prediction, probability = classify(review)

            st.session_state.review = review
            st.session_state.prediction = prediction
            st.session_state.probability = probability
            st.session_state.classified = True
            st.session_state.feedback_submitted = False
            st.session_state.step = 'feedback'
            st.rerun()
        else:
            st.warning("Please enter a review before submitting.")
elif st.session_state.step == 'feedback':
    results = st.subheader("Result")
    st.write(f"**Prediction:** {st.session_state.prediction}")
    st.write(f"**Probability:** {round(st.session_state.probability * 100, 2)}%")

    correct = st.header("Was this prediction correct?")
    feedback = st.radio("Please select an option: ", ("Correct", "Incorrect"), key = 'feedback_radio')

    submit_button = st.button("Submit Feedback")
    if submit_button:
        review = st.session_state.review
        prediction = st.session_state.prediction

        inv_label = {'negative': 0, 'positive': 1}
        y = inv_label[prediction]
        if feedback == 'Incorrect': y = int(not y)

        train(review, y)
        sqlite_entry(db, review, y)

        st.session_state.feedback_submitted = True
        st.session_state.step = 'done'
        st.rerun()
elif st.session_state.step == 'done':
    submission_success = st.success("Thanks for the feedback!")
    
    new_review = st.button("Submit New Review")
    if new_review:
        st.session_state.review = ""
        st.session_state.prediction = ""
        st.session_state.classified = False
        st.session_state.feedback_submitted = False
        st.session_state.step = 'input'
        st.rerun()