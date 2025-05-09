# Library imports
import streamlit as st
import numpy as np
import sqlite3
import pickle
import os

from vectorizer import vectorizer
from update import update_model

# Load the classifier model
current_directory = os.path.dirname(__file__)
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

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #D2B48C;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



st.set_page_config(
    page_title = 'Movie Review Sentiment Analysis'
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.title("Movie Review Sentiment Analysis")

st.header("Submit a Movie Review")
review = st.text_area("Enter your review here: ")

if st.button("Classify Review"):
    if review.strip():
        prediction, probability = classify(review)

        st.subheader("Result")
        st.write(f"**Prediction:** {prediction}")
        st.write(f"**Probability:** {round(probability * 100, 2)}%")

        st.session_state.review = review
        st.session_state.prediction = prediction
        st.session_state.classified = True
    else:
        st.warning("Please enter a review before submitting.")

if st.session_state.get('classified'):
    st.header("Was this prediction correct?")
    feedback = st.radio("Please select an option:", ('Correct', 'Incorrect'))

    if st.button('Submit Feedback'):
        review = st.session_state.review
        prediction = st.session_state.prediction

        inv_label = {'negative': 0, 'positive': 1}
        y = inv_label[prediction]
        if feedback == 'Incorrect': y = int(not y)

        train(review, y)
        sqlite_entry(db, review, y)
        st.success("Thanks for the feedback!")
