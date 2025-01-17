# Python imports
import os, sys
import sqlite3
from urllib.request import urlretrieve

# Third party imports
import pandas as pd


class DataSource:
    def __init__(self, file_name: str, url) -> None:
        self.file_name = file_name
        self.url = url


class DBConfig:
    def __init__(self, db_name: str, table_name: str) -> None:
        self.db_name = db_name
        self.table_name = table_name


class DataPipeline:
    def __init__(self, data_source: DataSource, output_db: DBConfig) -> None:
        self.data_source = data_source
        self.output_db = output_db

    def extract_data(self) -> str:
        file_path = os.path.join(os.getcwd(), self.data_source.file_name)
        try:
            urlretrieve(url=self.data_source.url, filename=file_path)
        except Exception as e:
            sys.exit(1)
        return file_path
    
    def transform_data(self, file_path: str) -> pd.DataFrame:
        data_frame = pd.read_csv(
            file_path, sep=";", header=0, names=None, compression=None, encoding="utf-8"
        )
        return data_frame

    def load_data(self, data_frame: pd.DataFrame) -> None:
        try:
            # connect to the database
            connection = sqlite3.connect(self.output_db.db_name)

            # insert data into the database
            data_frame.to_sql(
                self.output_db.table_name, connection, if_exists="replace", index=False
            )

            # close the connection
            connection.close()
        except sqlite3.Error as e:
            sys.exit(1)

    def run_pipeline(self) -> None:
        file_path = self.extract_data()
        data_frame = self.transform_data(file_path=file_path)
        self.load_data(data_frame=data_frame)


if __name__ == "__main__":
    data_source = DataSource(
        file_name="rhein-kreis-neuss-flughafen-weltweit.csv",
        url="https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv",
    )
    output_db = DBConfig(db_name="airports.sqlite", table_name="airports")
    etl_pipeline = DataPipeline(data_source=data_source, output_db=output_db)
    etl_pipeline.run_pipeline()
