# Python imports
import os

# Third-party imports
import numpy as np
import pandas as pd

# Self imports6
from services.pipeline import (
    ETLPipeline,
    DataSource,
    CSVFile,
    SQLiteDB,
)

if __name__ == "__main__":
    data_directory = os.path.join(os.getcwd(), "data")
    # Songs Pipeline
    songs_output_db = SQLiteDB(
        db_name="project.sqlite",
        table_name="song_lyrics",
        if_exists=SQLiteDB.REPLACE,
        index=False,
        method=None,
        output_directory=data_directory,
    )
    songs_file_dtype = {
        "#": "Int64",
        "artist": str,
        "seq": str,
        "song": str,
        "label": np.float64,
    }

    def transform_lyrics(data_frame: pd.DataFrame):
        data_frame = data_frame.drop(columns=data_frame.columns[0], axis=1)
        data_frame = data_frame.rename(columns={"seq": "lyrics"})
        return data_frame

    songs_file = CSVFile(
        file_name="labeled_lyrics_cleaned.csv",
        sep=",",
        names=None,
        dtype=songs_file_dtype,
        transform=transform_lyrics,
    )
    songs_data_source = DataSource(
        data_name="Song lyrics",
        url="https://www.kaggle.com/datasets/edenbd/150k-lyrics-labeled-with-spotify-valence",
        source_type=DataSource.KAGGLE_DATA,
        files=(songs_file,),
    )
    songs_pipeline = ETLPipeline(
        data_source=songs_data_source,
        sqlite_db=songs_output_db,
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
    twitter_pipeline = ETLPipeline(
        data_source=twitter_data_source,
        sqlite_db=twitter_output_db,
    )
    twitter_pipeline.run_pipeline()
