# Python imports
import logging
from typing import Callable, List, Iterable, Tuple, Any
import shutil
import os, sys
import sqlite3
from urllib.request import urlretrieve
from tqdm import tqdm

# Third-party imports
import pandas as pd
import opendatasets as od

# Self imports


class SQLiteDB:
    FAIL = "fail"
    REPLACE = "replace"
    APPEND = "append"

    def __init__(
        self,
        db_name: str,
        table_name: str,
        if_exists: str,
        index: bool,
        output_directory: str,
        method: Callable[
            [pd.DataFrame, sqlite3.Connection, List, Iterable[Tuple[Any]]], None
        ] = None,
    ) -> None:
        self.db_name = db_name
        self.table_name = table_name
        self.if_exists = if_exists
        self.index = index
        self.output_directory = output_directory
        self.method = method

    def _load_to_db(self, data_frame: pd.DataFrame):
        db_path = os.path.join(self.output_directory, self.db_name)
        try:
            connection = sqlite3.connect(db_path)
            data_frame.to_sql(
                self.table_name,
                connection,
                if_exists=self.if_exists,
                index=self.index,
                method=self.method,
            )
            connection.close()
        except sqlite3.Error as e:
            logging.error(msg=f"Error while creating SQLite DB: {e}")
            sys.exit(1)


class CSVFile:
    def __init__(
        self,
        file_name: str,
        sep: str,
        names: List[str],
        dtype: dict,
        transform: Callable[[pd.DataFrame], pd.DataFrame] = None,
        file_path=None,
        encoding="utf-8",
    ) -> None:
        self.file_name = file_name
        self.sep = sep
        self.names = names
        self.dtype = dtype
        self._transform = transform
        self.file_path = file_path
        self.encoding = encoding
        self._data_frame = None


class DataSource:
    KAGGLE_DATA_SOURCE = "kaggle"

    def __init__(
        self,
        data_name: str,
        url: str,
        source_name: str,
        files: Tuple[CSVFile],
    ) -> None:
        self.data_name = data_name
        self.url = url
        self.source_name = source_name
        self.files = files


class DataPipeline:
    def __init__(self, data_source: DataSource, sqlite_db: SQLiteDB = None) -> None:
        self.data_source = data_source
        self.sqlite_db = sqlite_db

    def _download_kaggle_zip_file(self) -> None:
        output_dir = self.sqlite_db.output_directory if self.sqlite_db else "."
        try:
            # urlretrieve(url=self.data_source.url, filename=output_path)
            od.download(
                dataset_id_or_url=self.data_source.url,
                data_dir=output_dir,
                force=False,
                dry_run=False,
            )
            dataset_id = od.utils.kaggle_direct.get_kaggle_dataset_id(
                dataset_id_or_url=self.data_source.url
            )
            id = dataset_id.split("/")[1]
            file_path = os.path.join(output_dir, id)
        except Exception as e:
            logging.error(msg=f"Error while downloading kaggle data: {e}")
            sys.exit(1)
        return file_path

    def _extract_data(self) -> str:
        if self.data_source.source_name == DataSource.KAGGLE_DATA_SOURCE:
            file_path = self._download_kaggle_zip_file()
        return file_path

    def _transform_data(self, file: CSVFile) -> pd.DataFrame:
        data_frame = pd.read_csv(
            file.file_path,
            sep=file.sep,
            header=0,
            names=None,
            compression=None,
            dtype=file.dtype,
            encoding=file.encoding,
        )
        if file._transform:
            data_frame = file._transform(data_frame=data_frame)
        return data_frame

    def _load_data(self, file: CSVFile) -> None:
        if self.sqlite_db != None:
            self.sqlite_db._load_to_db(data_frame=file._data_frame)

    def run_pipeline(self) -> None:
        print(f"Running pipeling for {self.data_source.data_name} ....")
        file_path = self._extract_data()
        tqdm_files = tqdm(self.data_source.files)
        for item in tqdm_files:
            tqdm_files.set_description(f"Processing {item.file_name}")
            item.file_path = os.path.join(os.getcwd(), file_path, item.file_name)
            item._data_frame = self._transform_data(file=item)
            self._load_data(file=item)
        shutil.rmtree(file_path)
