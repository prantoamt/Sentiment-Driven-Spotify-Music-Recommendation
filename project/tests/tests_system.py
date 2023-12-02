# Python imports
import os, sys
import logging
# Third-party imports
import sqlite3
import pandas as pd
from pandas.testing import assert_frame_equal

# Self imports
from etl_pipeline_runner.services import (
    ETLQueue,
)

class TestPipeline:
    def test_song_pipline_ok(self, songs_pipeline):
        loader = songs_pipeline.extractor.file_handlers[0].loader
        ETLQueue(etl_pipelines=(songs_pipeline,)).run()
        db_path = os.path.join(loader.output_directory, loader.db_name)
        try:
            connection = sqlite3.connect(db_path)
            result = pd.read_sql_query(f"SELECT * FROM {loader.table_name}", connection)
        except sqlite3.Error as e:
            logging.error(msg=f"Error while creating SQLite DB: {e}")
            sys.exit(1)
        finally:
            connection.close()
        transformed_data = songs_pipeline.extractor.file_handlers[0]._data_frame
        assert_frame_equal(result, transformed_data)
        os.remove(db_path)

    def test_twitter_pipline_ok(self, twitter_pipeline):
        loader = twitter_pipeline.extractor.file_handlers[0].loader
        ETLQueue(etl_pipelines=(twitter_pipeline,)).run()
        db_path = os.path.join(loader.output_directory, loader.db_name)
        try:
            connection = sqlite3.connect(db_path)
            result = pd.read_sql_query(f"SELECT * FROM {loader.table_name}", connection)
        except sqlite3.Error as e:
            logging.error(msg=f"Error while creating SQLite DB: {e}")
            sys.exit(1)
        finally:
            connection.close()
        transformed_data = twitter_pipeline.extractor.file_handlers[0]._data_frame
        assert_frame_equal(result, transformed_data)
        os.remove(db_path)