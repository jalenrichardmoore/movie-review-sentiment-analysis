# Library imports
import sqlite3
import os

# Create a SQLite database
conn = sqlite3.connect('reviews.sqlite')
connection = conn.cursor()
connection.execute('DROP TABLE IF EXISTS review_db')
connection.execute('CREATE TABLE review_db (review TEXT, sentiment INTEGER, date TEXT)')

# Add example of positive movie review to database
example_01 = 'I love this movie'
connection.execute("INSERT INTO review_db (review, sentiment, date) VALUES (?, ?, DATETIME('now'))", (example_01, 1))

# Add example of negative movie review to database
example_02 = 'I disliked this movie'
connection.execute("INSERT INTO review_db (review, sentiment, date) VALUES (?, ?, DATETIME('now'))", (example_02, 0))

# Close the connection to the database
conn.commit()
conn.close()