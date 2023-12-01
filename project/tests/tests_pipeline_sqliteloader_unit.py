# Python imports
import os
import sqlite3
import pytest
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
    
def test_sqlite_loader_replace_if_exists_ok():
    db_name = "test_sqlite_loader.sqlite"
    table_name = "loader_table"
    data_frame = pd.DataFrame(
        data={'col1': [1, 2], 'col2': [3, 4]},
        dtype=np.int64,
        )
    db_path = os.path.join(DATA_DIRECTORY, db_name)
    loader = SQLiteLoader(
        db_name=db_name,
        table_name=table_name,
        if_exists=SQLiteLoader.REPLACE,
        index=None,
        method=None,
        output_directory=DATA_DIRECTORY,
        )
    loader._load_to_db(data_frame=data_frame)
    loader._load_to_db(data_frame=data_frame)
    connection = sqlite3.connect(db_path)
    result = pd.read_sql_query(f"SELECT * FROM {loader.table_name}", connection)
    assert_frame_equal(result, data_frame)
    os.remove(db_path)
    

def test_sqlite_loader_append_if_exists_ok():
    db_name = "test_sqlite_loader.sqlite"
    table_name = "loader_table"
    data_frame = pd.DataFrame(
        data={'col1': [1, 2], 'col2': [3, 4]},
        dtype=np.int64,
        )
    appended_data_frame = pd.concat([data_frame, data_frame], ignore_index=True)
    db_path = os.path.join(DATA_DIRECTORY, db_name)
    loader = SQLiteLoader(
        db_name=db_name,
        table_name=table_name,
        if_exists=SQLiteLoader.APPEND,
        index=None,
        method=None,
        output_directory=DATA_DIRECTORY,
        )
    loader._load_to_db(data_frame=data_frame)
    loader._load_to_db(data_frame=data_frame)
    connection = sqlite3.connect(db_path)
    result = pd.read_sql_query(f"SELECT * FROM {loader.table_name}", connection)
    assert_frame_equal(result, appended_data_frame)
    os.remove(db_path)
    
def test_sqlite_loader_fail_if_exists_ok():
    db_name = "test_sqlite_loader.sqlite"
    table_name = "loader_table"
    data_frame = pd.DataFrame(
        data={'col1': [1, 2], 'col2': [3, 4]},
        dtype=np.int64,
        )
    appended_data_frame = pd.concat([data_frame, data_frame], ignore_index=True)
    db_path = os.path.join(DATA_DIRECTORY, db_name)
    loader = SQLiteLoader(
        db_name=db_name,
        table_name=table_name,
        if_exists=SQLiteLoader.FAIL,
        index=None,
        method=None,
        output_directory=DATA_DIRECTORY,
        )
    loader._load_to_db(data_frame=data_frame)
    with pytest.raises(Exception):
        loader._load_to_db(data_frame=data_frame)
    os.remove(db_path)