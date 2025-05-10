# **Movie Review Sentiment Analysis**

## **Overview**
A Python application that allows users to enter in movie reviews and then have a machine learning algorithm use sentiment analysis to determine if that review is either positive or negative. Submitted reviews are then added to a database for future training.

## **Folder Structure**
```plaintext
movie-review-sentiment-analysis/
│
├── .streamlit/
│   └── config.toml                       # Config for Streamlit app (background color, text color)
│
├── app/
│   ├── __init__.py
│   └── app.py                            # Streamlit app script
│
├── datasets/
│   └── movie_data.csv                    # Movie review dataset for initial model
│
├── movie_classifier/
│   ├── __init__.py              
│   ├── movie_classifier.py               # Script to create the initial model off the dataset and store it
│   ├── reviews_database.py               # Script to create the database of movie reviews
│   ├── update.py                         # Defines function to update the model when a new review is analyzed
│   ├── vectorizer.py                     # Defines vectorizer used in the model to process text input
│   └── pkl_objects/
│       ├── classifier.pkl                # Pickled sentiment classifier model
│       └── stopwords.pkl                 # Pickled list of stopwords used in text processing
│
├── reviews.sqlite                        # Database of movie reviews
├── requirements.txt                      # List of dependencies for Streamlit app
├── run.py                                # Cross-platform launcher script (sets up env and runs app)
└── README.md
```

## **Dependencies**
- Python 3.9 or higher installed (https://www.python.org/downloads/)
- Internet connection (for installing packages)

## **Installation & Usage**
1. Clone the repository:
```sh
git clone https://github.com/Jalen-Moore/stranded-scripts.git
```

2. From your terminal, in the root folder of the project, run:
   ```sh
   python run.py
   ```
   
## **Credits**
Developed by Jalen Moore
