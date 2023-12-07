# Python imports
import os

# Third party imports
import pytest
import numpy as np
import pandas as pd

# Self imports
from etl_pipeline_runner.services import (
    ETLPipeline,
    DataExtractor,
    CSVHandler,
    SQLiteLoader,
    ETLQueue,
)

DATA_DIRECTORY = os.path.join(os.getcwd(), "data")

@pytest.fixture
def songs_pipeline():
    songs_loader = SQLiteLoader(
    db_name="test.sqlite",
    table_name="songs",
    if_exists=SQLiteLoader.REPLACE,
    index=False,
    method=None,
    output_directory=DATA_DIRECTORY,
    )
    songs_file_dtype = {
        "track_name": str,
        "artist(s)_name": str,
        "artist_count": np.int64,
        "released_year": np.int64,
        "released_month": np.int64,
        "released_day": np.int64,
        "in_spotify_playlists": np.int64,
        "in_spotify_charts": np.int64,
        "streams": np.int64,
        "in_apple_playlists": np.int64,
        "in_apple_charts": np.int64,
        "in_deezer_playlists": np.int64,
        "in_deezer_charts": np.int64,
        "in_shazam_charts": np.int64,
        "bpm": np.int64,
        "key": str,
        "mode": str,
        "danceability_%": np.int64,
        "valence_%": np.int64,
        "energy_%": np.int64,
        "acousticness_%": np.int64,
        "instrumentalness_%": np.int64,
        "liveness_%": np.int64,
        "speechiness_%": np.int64,
    }
    
    def transform_songs(data_frame: pd.DataFrame):
        data_frame = data_frame.drop(columns=data_frame.columns[0], axis=1)
        return data_frame

    songs_csv_handler = CSVHandler(
        file_name="spotify-2023.csv",
        sep=",",
        names=None,
        transformer=transform_songs,
        loader=songs_loader,
        encoding="latin-1",
    )
    songs_data_extractor = DataExtractor(
        data_name="Spotify songs",
        url="https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023",
        type=DataExtractor.KAGGLE_ARCHIVE,
        file_handlers=(songs_csv_handler,),
    )
    songs_pipeline = ETLPipeline(
        extractor=songs_data_extractor,
    )
    yield songs_pipeline
    

@pytest.fixture
def twitter_pipeline():
    twitter_output_db = SQLiteLoader(
        db_name="test.sqlite",
        table_name="tweets",
        if_exists=SQLiteLoader.REPLACE,
        index=False,
        method=None,
        output_directory=DATA_DIRECTORY,
    )
    
    def transform_twitter(data_frame: pd.DataFrame):
        data_frame = data_frame.dropna(axis=0)
        data_frame = data_frame.drop(columns=[data_frame.columns[1], data_frame.columns[2], data_frame.columns[3], data_frame.columns[4]], axis=1)
        data_frame = data_frame.replace({"target": {4:1}})
        return data_frame
    
    twitter_csv_handler = CSVHandler(
        file_name="training.1600000.processed.noemoticon.csv",
        sep=",",
        names=["target", "id", "date", "flag", "user", "text"],
        dtype={"target": np.int64, "text": str},
        encoding="ISO-8859-1",
        transformer=transform_twitter,
        loader=twitter_output_db
    )
    
    twitter_data_extractor = DataExtractor(
        data_name="Twitter",
        url="https://www.kaggle.com/datasets/kazanova/sentiment140",
        type=DataExtractor.KAGGLE_ARCHIVE,
        file_handlers=(twitter_csv_handler,),
    )
    
    twitter_pipeline = ETLPipeline(
        extractor=twitter_data_extractor,
    )
    
    yield twitter_pipeline
    
@pytest.fixture
def mock_tweet_df():
    data = [
        [0,"1467810369","Mon Apr 06 22:19:45 PDT 2009","NO_QUERY","_TheSpecialOne_","This is a mock tweet with target 0 which contains one @user tag, one link: https://github.com/prantoamt/made-template, and several special characters. For exmaple: # :( :)."],
        [4,"1467810369","Mon Apr 06 22:19:45 PDT 2009","NO_QUERY","_TheSpecialOne_","This is another mock tweet with target 1 which contains one @user tag, one link: https://github.com/prantoamt/made-template, and several special characters. For exmaple: # :( :)."]
        ]
    df = pd.DataFrame(
        data=data,
        columns=["target", "id", "date", "flag", "user", "text"],
    )
    return df