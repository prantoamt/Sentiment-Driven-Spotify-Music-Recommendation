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
    table_name="song_lyrics",
    if_exists=SQLiteLoader.REPLACE,
    index=False,
    method=None,
    output_directory=DATA_DIRECTORY,
    )
    songs_dtype = {
        "#": "Int64",
        "artist": str,
        "seq": str,
        "song": str,
        "label": np.float64,
    }
    
    def transform_songs(data_frame: pd.DataFrame):
        data_frame = data_frame.drop(columns=data_frame.columns[0], axis=1)
        data_frame = data_frame.rename(columns={"seq": "lyrics"})
        return data_frame

    songs_csv_handler = CSVHandler(
        file_name="labeled_lyrics_cleaned.csv",
        sep=",",
        names=None,
        dtype=songs_dtype,
        transformer=transform_songs,
        loader=songs_loader,
    )

    songs_extractor = DataExtractor(
        data_name="Song lyrics",
        url="https://www.kaggle.com/datasets/edenbd/150k-lyrics-labeled-with-spotify-valence",
        type=DataExtractor.KAGGLE_ARCHIVE,
        file_handlers=(songs_csv_handler,),
    )

    songs_pipeline = ETLPipeline(
        extractor=songs_extractor,
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
    twitter_file_dtype = {
        "clean_text": str,
        "category": np.float64,
    }
    twitter_csv_handler = CSVHandler(
        file_name="Twitter_Data.csv",
        sep=",",
        names=None,
        dtype=twitter_file_dtype,
        transformer=None,
        loader=twitter_output_db
    )
    twitter_data_extractor = DataExtractor(
        data_name="Twitter",
        url="https://www.kaggle.com/datasets/saurabhshahane/twitter-sentiment-dataset/",
        type=DataExtractor.KAGGLE_ARCHIVE,
        file_handlers=(twitter_csv_handler,),
    )
    twitter_pipeline = ETLPipeline(
        extractor=twitter_data_extractor,
    )
    yield twitter_pipeline
    
@pytest.fixture
def sqlite_loader(**kwargs):
    def _sqlite_loader(**kwargs):
        db_name = "test_sqlite_loader.sqlite"
        table_name = "loader_table"
        if_exists = kwargs.pop("if_exists")
        sqlite_loader = SQLiteLoader(
            db_name=db_name,
            table_name=table_name,
            if_exists=if_exists,
            index=None,
            method=None,
            output_directory=DATA_DIRECTORY,
        )
        return sqlite_loader
    return _sqlite_loader