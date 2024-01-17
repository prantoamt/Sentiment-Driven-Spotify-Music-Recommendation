from joblib import load
import logging, sys
import pandas as pd
import sqlite3
from services.song_recommendation_engine import SongsRecommendationEngine



if __name__ == "__main__":
    try:
        connection = sqlite3.connect("./data/project.sqlite")
        songs = pd.read_sql_query(f"SELECT * FROM songs", connection)
        user_playlist = pd.read_sql_query(f"SELECT * FROM user_playlist", connection)
    except sqlite3.Error as e:
        logging.error(msg=f"Error while creating SQLite DB: {e}")
        sys.exit(1)
    finally:
        connection.close()
    recommendation_engine = SongsRecommendationEngine(all_songs=songs, user_playlist=user_playlist)
    sentiment_map = {
        0: "Sad",
        1: "Happy",
    }
    vectorizer = load('project/vectorizer.joblib')
    lr_model = load('project/logistic_regression_model.joblib') 
    while True:
        tweet = input('Make a new post in tweeter: ')
        tweet = vectorizer.transform([tweet])
        sentiment = lr_model.predict(tweet)
        recommended_song = recommendation_engine.recommend_song(sentiment=sentiment).iloc[0] 
        print()
        print(f"Seems like you are {sentiment_map.get(sentiment[0])}! The song '{recommended_song['track_name']}' by {recommended_song['artist(s)_name']} released in {recommended_song['released_year']} may allign with your mood.")
        print()