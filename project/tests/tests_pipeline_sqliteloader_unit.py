# Python imports
import os
import sqlite3
import pytest
# Third-party imports
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

# Self imports
from project.tests.conftest import DATA_DIRECTORY
from etl_pipeline_runner.services import (
    SQLiteLoader,
)

class TestSqliteLoader:   
    def test_sqlite_loader_replace_if_exists_ok(self, sqlite_loader):
        sqlite_loader = sqlite_loader(if_exists=SQLiteLoader.REPLACE)
        data_frame = pd.DataFrame(
            data={'col1': [1, 2], 'col2': [3, 4]},
            dtype=np.int64,
        )
        db_path = os.path.join(DATA_DIRECTORY, sqlite_loader.db_name)
        sqlite_loader._load_to_db(data_frame=data_frame)
        sqlite_loader._load_to_db(data_frame=data_frame)
        connection = sqlite3.connect(db_path)
        result = pd.read_sql_query(
            f"SELECT * FROM {sqlite_loader.table_name}",
            connection
        )
        assert_frame_equal(result, data_frame)
        os.remove(db_path)
        

    def test_sqlite_loader_append_if_exists_ok(self, sqlite_loader):
        sqlite_loader = sqlite_loader(if_exists=SQLiteLoader.APPEND)
        data_frame = pd.DataFrame(
            data={'col1': [1, 2], 'col2': [3, 4]},
            dtype=np.int64,
            )
        appended_data_frame = pd.concat(
            [data_frame, data_frame],
            ignore_index=True,
        )
        db_path = os.path.join(DATA_DIRECTORY, sqlite_loader.db_name)
        sqlite_loader._load_to_db(data_frame=data_frame)
        sqlite_loader._load_to_db(data_frame=data_frame)
        connection = sqlite3.connect(db_path)
        result = pd.read_sql_query(f"SELECT * FROM {sqlite_loader.table_name}", connection)
        assert_frame_equal(result, appended_data_frame)
        os.remove(db_path)
        
    def test_sqlite_loader_fail_if_exists_ok(self, sqlite_loader):
        sqlite_loader = sqlite_loader(if_exists=SQLiteLoader.FAIL)
        data_frame = pd.DataFrame(
            data={'col1': [1, 2], 'col2': [3, 4]},
            dtype=np.int64,
            )
        db_path = os.path.join(DATA_DIRECTORY, sqlite_loader.db_name)
        sqlite_loader._load_to_db(data_frame=data_frame)
        with pytest.raises(Exception):
            sqlite_loader._load_to_db(data_frame=data_frame)
        os.remove(db_path)