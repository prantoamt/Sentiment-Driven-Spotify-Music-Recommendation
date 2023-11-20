# Python imports
import os

# Third-party imports
import numpy as np
import pandas as pd

# Self imports6
from services.pipeline import (
    DataPipeline,
    DataSource,
    CSVFile,
    SQLiteDB,
)

if __name__ == "__main__":
    data_directory = os.path.join(os.getcwd(), "data")
    # Songs Pipeline
    genres_output_db = SQLiteDB(
        db_name="project.sqlite",
        table_name="genres",
        if_exists=SQLiteDB.REPLACE,
        index=False,
        method=None,
        output_directory=data_directory,
    )
    genres_file_dtype = {
        "danceability": np.float64,
        "energy": np.float64,
        "key": "Int64",
        "loudness": np.float64,
        "mode": "Int64",
        "speechiness": np.float64,
        "acousticness": np.float64,
        "instrumentalness": np.float64,
        "liveness": np.float64,
        "valence": np.float64,
        "tempo": np.float64,
        "type": str,
        "id": str,
        "uri": str,
        "track_href": str,
        "analysis_url": str,
        "duration_ms": "Int64",
        "time_signature": "Int64",
        "genre": str,
        "song_name": str,
        "Unnamed: 0": np.float64,
        "title": str,
    }

    genres_file = CSVFile(
        file_name="genres_v2.csv",
        sep=",",
        names=None,
        dtype=genres_file_dtype,
    )
    songs_data_source = DataSource(
        data_name="Spotify Songs",
        url="https://www.kaggle.com/datasets/mrmorj/dataset-of-songs-in-spotify/data",
        source_type=DataSource.KAGGLE_DATA,
        files=(genres_file,),
    )
    songs_pipeline = DataPipeline(
        data_source=songs_data_source,
        sqlite_db=genres_output_db,
    )
    songs_pipeline.run_pipeline()

    # Twitter Pipeline
    twitter_output_db = SQLiteDB(
        db_name="project.sqlite",
        table_name="tweets",
        if_exists=SQLiteDB.REPLACE,
        index=False,
        method=None,
        output_directory=data_directory,
    )
    twitter_file_dtype = {
        "clean_text": str,
        "category": "Int64",
    }
    twitter_file = CSVFile(
        file_name="Twitter_Data.csv",
        sep=",",
        names=None,
        dtype=twitter_file_dtype,
    )
    twitter_data_source = DataSource(
        data_name="Twitter",
        url="https://www.kaggle.com/datasets/saurabhshahane/twitter-sentiment-dataset/",
        source_type=DataSource.KAGGLE_DATA,
        files=(twitter_file,),
    )
    twitter_pipeline = DataPipeline(
        data_source=twitter_data_source,
        sqlite_db=twitter_output_db,
    )
    twitter_pipeline.run_pipeline()