# Python imports
import shutil
import os, sys
import sqlite3
from urllib.request import urlretrieve

# Third-party imports
import pandas as pd
import opendatasets as od

# Self imports


class OutputDBConfig:
    def __init__(self, db_name: str, table_name: str) -> None:
        self.db_name = db_name
        self.table_name = table_name


class CSVFile:
    def __init__(
        self,
        file_name: str,
        sep: str,
        names: list[str],
        output_db: OutputDBConfig,
        dtype: dict,
        file_path=None,
        encoding="utf-8",
    ) -> None:
        self.file_name = file_name
        self.sep = sep
        self.names = names
        self.output_db = output_db
        self.dtype = dtype
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
        files_type: str,
    ) -> None:
        self.url = url
        self.source_name = source_name
        self.files = files
        self.files_type = files_type


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
        return data_frame

    def _load_data(self, file: CSVFile) -> None:
        db_path = os.path.join(os.getcwd(), "data", file.output_db.db_name)
        try:
            connection = sqlite3.connect(db_path)
            file._data_frame.to_sql(
                file.output_db.table_name, connection, if_exists="replace", index=False
            )
            connection.close()
        except sqlite3.Error as e:
            sys.exit(1)

    def run_pipeline(self) -> None:
        print(f"Running pipeling for {self.data_source.url} ....")
        file_path = self._extract_data()
        for item in self.data_source.files:
            item.file_path = os.path.join(os.getcwd(), file_path, item.file_name)
            item._data_frame = self._transform_data(file=item)
            self._load_data(file=item)
        shutil.rmtree(file_path)