# Python imports
import random

# Third party imports
import pandas as pd

# Self imports


class SongsRecommendationEngine:
    def __init__(self, all_songs: pd.DataFrame, user_playlist: pd.DataFrame) -> None:
        self.audio_features_avg = {
            "bpm": 0,
            "danceability_%": 0,
            "energy_%": 0,
            "acousticness_%": 0,
            "instrumentalness_%": 0, 
            "liveness_%": 0,
            "speechiness_%": 0
        }
        self.all_songs = all_songs.copy()
        self.user_playlist = user_playlist.copy()
        for item in self.user_playlist["track_name"].values:
            self.all_songs = self.remove_subset_of_df(item)
    
    
    def remove_subset_of_df(self, identifier_to_be_removed: str):
        mask = self.all_songs["track_name"] == identifier_to_be_removed
        return self.all_songs[~mask]
    
    def calculate_avg_of_audio_features(self, songs: pd.DataFrame):
        for key, value in self.audio_features_avg.items():
            self.audio_features_avg[key] = songs[key].mean()

    def get_songs_aligned_with_audio_features_and_sentiment(self, sentiment: int):
        plus_minus_range = 15
        recommend_songs = self.all_songs.copy()
        if sentiment == 0:
            recommend_songs =  recommend_songs[recommend_songs["valence_%"] < 50]
        elif sentiment == 1:
            recommend_songs =  recommend_songs[recommend_songs["valence_%"] > 50]
            
        feature, _ = random.choice(list(self.audio_features_avg.items()))
        recommend_songs = recommend_songs[(recommend_songs["bpm"] > self.audio_features_avg["bpm"] - plus_minus_range) & (recommend_songs["bpm"] < self.audio_features_avg["bpm"] +plus_minus_range)]
        recommend_songs = recommend_songs[(recommend_songs["danceability_%"] > self.audio_features_avg["danceability_%"] - plus_minus_range) & (recommend_songs["danceability_%"] < self.audio_features_avg["danceability_%"] +plus_minus_range)]
        recommend_songs = recommend_songs[(recommend_songs["energy_%"] > self.audio_features_avg["energy_%"] - plus_minus_range) & (recommend_songs["energy_%"] < self.audio_features_avg["energy_%"] +plus_minus_range)]
        recommend_songs = recommend_songs[(recommend_songs["acousticness_%"] > self.audio_features_avg["acousticness_%"] - plus_minus_range) & (recommend_songs["acousticness_%"] < self.audio_features_avg["acousticness_%"] +plus_minus_range)]
        recommend_songs = recommend_songs[(recommend_songs["speechiness_%"] > self.audio_features_avg["speechiness_%"] - plus_minus_range) & (recommend_songs["speechiness_%"] < self.audio_features_avg["speechiness_%"] +plus_minus_range)]
        recommend_songs = recommend_songs[(recommend_songs["liveness_%"] > self.audio_features_avg["liveness_%"] - plus_minus_range) & (recommend_songs["liveness_%"] < self.audio_features_avg["liveness_%"] +plus_minus_range)]
        recommend_songs = recommend_songs[(recommend_songs["instrumentalness_%"] > self.audio_features_avg["instrumentalness_%"] - plus_minus_range) & (recommend_songs["instrumentalness_%"] < self.audio_features_avg["instrumentalness_%"] +plus_minus_range)]
        recommend_songs = recommend_songs.sort_values(feature, ascending=False)
        return recommend_songs
    
    def recommend_song(self, sentiment: int) -> pd.DataFrame:
        songs_aligned_with_sentiment = None
        if sentiment == 0:
            songs_aligned_with_sentiment = self.user_playlist[self.user_playlist["valence_%"] < 50]
        elif sentiment == 1:
            songs_aligned_with_sentiment = self.user_playlist[self.user_playlist["valence_%"] > 50]
        
        self.calculate_avg_of_audio_features(songs=songs_aligned_with_sentiment)
        
        recommended_songs = self.get_songs_aligned_with_audio_features_and_sentiment(sentiment=sentiment)
        return recommended_songs.sample(1)