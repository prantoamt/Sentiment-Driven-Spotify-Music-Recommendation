# Python imports
import os
import sqlite3
# Third-party imports
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

# Self imports6
from etl_pipeline_runner.services import (
    ETLPipeline,
    DataExtractor,
    CSVHandler,
    SQLiteLoader,
    ETLQueue,
)

DATA_DIRECTORY = os.path.join(os.getcwd(), "data")
    
songs_loader = SQLiteLoader(
    db_name="test.sqlite",
    table_name="song_lyrics",
    if_exists=SQLiteLoader.REPLACE,
    index=False,
    method=None,
    output_directory=DATA_DIRECTORY,
)

twitter_loader = SQLiteLoader(
    db_name="test.sqlite",
    table_name="twitter",
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


def test_song_pipline_ok():
    ETLQueue(etl_pipelines=(songs_pipeline,)).run()
    db_path = os.path.join(songs_loader.output_directory, songs_loader.db_name)
    connection = sqlite3.connect(db_path)
    result = pd.read_sql_query(f"SELECT * FROM {songs_loader.table_name}", connection)
    connection.close()
    data = songs_pipeline.extractor.file_handlers[0]._data_frame
    assert_frame_equal(result, data)
    os.remove(db_path)

def test_twitter_pipline_ok():
    ETLQueue(etl_pipelines=(twitter_pipeline,)).run()
    db_path = os.path.join(twitter_output_db.output_directory, twitter_output_db.db_name)
    connection = sqlite3.connect(db_path)
    result = pd.read_sql_query(f"SELECT * FROM {twitter_output_db.table_name}", connection)
    connection.close()
    data = twitter_pipeline.extractor.file_handlers[0]._data_frame
    assert_frame_equal(result, data)
    os.remove(db_path)