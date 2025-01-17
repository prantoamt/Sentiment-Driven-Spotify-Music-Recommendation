# Python imports
import os, re

# Third-party imports
import numpy as np
import pandas as pd
from nltk import download as nltkdownload
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

# Self imports6
from etl_pipeline_runner.services import (
    ETLPipeline,
    DataExtractor,
    CSVHandler,
    SQLiteLoader,
    ETLQueue,
)

DATA_DIRECTORY = os.path.join(os.getcwd(), "data")

nltkdownload("stopwords")
nltkdownload('punkt')
nltkdownload('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()
def preprocess(data):
    # @user remove
    processed_data = re.sub("@\w+", " ", data)
    # link remove
    processed_data = re.sub(r'http\S+', '', processed_data)
    # special character and number remove
    processed_data = re.sub("[^a-zA-Z]", " ", processed_data)
    # single character remove
    processed_data = re.sub(r"\s+[a-zA-Z]\s+", " ", processed_data)
    # multiple space remove
    processed_data = re.sub(r"\s+", " ", processed_data)
    processed_data = processed_data.lower()
    processed_data = word_tokenize(processed_data)
    processed_data = [wordnet_lemmatizer.lemmatize(word) for word in processed_data if word not in stopwords.words("english")]
    processed_data = " ".join(processed_data)
    return processed_data

def construct_songs_pipeline() -> ETLPipeline:
    songs_loader = SQLiteLoader(
        db_name="project.sqlite",
        table_name="songs",
        if_exists=SQLiteLoader.REPLACE,
        index=False,
        method=None,
        output_directory=DATA_DIRECTORY,
    )

    def transform_songs(data_frame: pd.DataFrame):
        data_frame = data_frame.dropna(axis=0)
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
    
    def transform_twitter(data_frame: pd.DataFrame):
        data_frame = data_frame.dropna(axis=0)
        data_frame = data_frame.drop(columns=[data_frame.columns[1], data_frame.columns[2], data_frame.columns[3], data_frame.columns[4]], axis=1)
        data_frame = data_frame.replace({"target": {4:1}})
        data_frame["processed_text"] = data_frame["text"].apply(preprocess)
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
    return twitter_pipeline


if __name__ == "__main__":
    songs_pipeline = construct_songs_pipeline()
    twitter_pipeline = construct_twitter_pipeline()
    pipeline_queue = ETLQueue(etl_pipelines=(twitter_pipeline, songs_pipeline,)).run()
