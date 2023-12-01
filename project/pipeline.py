# Python imports
import os

# Third-party imports
import numpy as np
import pandas as pd

# Self imports6
from etl_pipeline_runner.services import (
    ETLPipeline,
    DataExtractor,
    CSVHandler,
    SQLiteLoader,
    ETLQueue,
)

DATA_DIRECTORY = os.path.join(os.getcwd(), "data")

def construct_songs_pipeline() -> ETLPipeline:
    songs_output_db = SQLiteLoader(
        db_name="project.sqlite",
        table_name="song_lyrics",
        if_exists=SQLiteLoader.REPLACE,
        index=False,
        method=None,
        output_directory=DATA_DIRECTORY,
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

    songs_csv_handler = CSVHandler(
        file_name="labeled_lyrics_cleaned.csv",
        sep=",",
        names=None,
        dtype=songs_file_dtype,
        transformer=transform_lyrics,
        loader=songs_output_db
    )
    songs_data_extractor = DataExtractor(
        data_name="Song lyrics",
        url="https://www.kaggle.com/datasets/edenbd/150k-lyrics-labeled-with-spotify-valence",
        type=DataExtractor.KAGGLE_ARCHIVE,
        file_handlers=(songs_csv_handler,),
    )
    songs_pipeline = ETLPipeline(
        extractor=songs_data_extractor,
    )
    return songs_pipeline


def construct_twitter_pipeline() -> ETLPipeline:
    twitter_output_db = SQLiteLoader(
        db_name="project.sqlite",
        table_name="tweets",
        if_exists=SQLiteLoader.REPLACE,
        index=False,
        method=None,
        output_directory=DATA_DIRECTORY,
    )
    twitter_file_dtype = {
        "clean_text": str,
        "category": "Int64",
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
    return twitter_pipeline


if __name__ == "__main__":
    songs_pipeline = construct_songs_pipeline()
    twitter_pipeline = construct_twitter_pipeline()
    pipeline_queue = ETLQueue(etl_pipelines=(songs_pipeline, twitter_pipeline)).run()
