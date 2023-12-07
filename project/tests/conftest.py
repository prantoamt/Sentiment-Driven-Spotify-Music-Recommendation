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
from project.pipeline import construct_songs_pipeline, construct_twitter_pipeline

DATA_DIRECTORY = os.path.join(os.getcwd(), "data")

@pytest.fixture
def songs_pipeline():
    songs_pipeline = construct_songs_pipeline()
    songs_pipeline.extractor.file_handlers[0].transformer = None
    songs_pipeline.extractor.file_handlers[0].loader.db_name = "test.sqlite"
    yield songs_pipeline
    

@pytest.fixture
def twitter_pipeline():
    twitter_pipeline = construct_twitter_pipeline()
    twitter_pipeline.extractor.file_handlers[0].transformer = None
    twitter_pipeline.extractor.file_handlers[0].loader.db_name = "test.sqlite"
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