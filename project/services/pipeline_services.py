# Python imports
from typing import Callable
import shutil
import os, sys
import sqlite3
from urllib.request import urlretrieve

# Third-party imports
import pandas as pd
import opendatasets as od

# Self imports


class SQLiteDB:
    def __init__(
        self,
        db_name: str,
        table_name: str,
        if_exists: str,
        index: bool,
        method: Callable,
    ) -> None:
        self.db_name = db_name
        self.table_name = table_name
        self.if_exists = if_exists
        self.index = index
        self.method = method
    
    def _load_to_db(self, output_dir: str, data_frame: pd.DataFrame):
        db_path = os.path.join(output_dir, self.db_name)
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
            sys.exit(1)


class CSVFile:
    def __init__(
        self,
        file_name: str,
        sep: str,
        names: list[str],
        dtype: dict,
        transform: Callable[[pd.DataFrame], pd.DataFrame] = None,
        file_path=None,
        encoding="utf-8",
        sqlite_db: SQLiteDB = None,
    ) -> None:
        self.file_name = file_name
        self.sep = sep
        self.names = names
        self.sqlite_db = sqlite_db
        self.dtype = dtype
        self._transform = transform
        self.file_path = file_path
        self.encoding = encoding
        self._data_frame = None


class DataSource:
    KAGGLE_DATA_SOURCE = "kaggle"

    def __init__(
        self,
        url: str,
        source_name: str,
        files: list[CSVFile],
    ) -> None:
        self.url = url
        self.source_name = source_name
        self.files = files


class DataPipeline:
    def __init__(self, data_source: DataSource) -> None:
        self.data_source = data_source

    def __download_kaggle_zip_file(self) -> None:
        data_dir = "data"
        try:
            # urlretrieve(url=self.data_source.url, filename=output_path)
            od.download(
                dataset_id_or_url=self.data_source.url,
                data_dir=data_dir,
                force=False,
                dry_run=False,
            )
            dataset_id = od.utils.kaggle_direct.get_kaggle_dataset_id(
                dataset_id_or_url=self.data_source.url
            )
            id = dataset_id.split("/")[1]
            file_path = os.path.join(data_dir, id)
        except Exception as e:
            print(e)
            sys.exit(1)
        return file_path

    def _extract_data(self) -> str:
        if self.data_source.source_name == DataSource.KAGGLE_DATA_SOURCE:
            file_path = self.__download_kaggle_zip_file()
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
        output_dir = os.path.join(os.getcwd(), "data")
        if file.sqlite_db != None:
            file.sqlite_db._load_to_db(output_dir=output_dir, data_frame=file._data_frame)

    def run_pipeline(self) -> None:
        print(f"Running pipeling for {self.data_source.url} ....")
        file_path = self._extract_data()
        for item in self.data_source.files:
            item.file_path = os.path.join(os.getcwd(), file_path, item.file_name)
            item._data_frame = self._transform_data(file=item)
            self._load_data(file=item)
        shutil.rmtree(file_path)
