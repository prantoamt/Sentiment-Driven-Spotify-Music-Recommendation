# Python imports
import numpy as np
# Third-party imports

# Self imports6
from services.pipeline_services import (
    DataPipeline,
    DataSource,
    FileInfo,
    OutputDBConfig,
)

if __name__ == "__main__":
    genres_output_db = OutputDBConfig(db_name="project.sqlite", table_name="genres")
    genres_file_dtype = {
        "danceability": np.float64,
        "energy": np.float64,
        "key": "Int64",
        "loudness": np.float64,
        "mode": "Int64",
        "speechiness": np.float64,
        "acousticness": np.float64,
        "instrumentalness": np.float64,
        "liveness": np.float64,
        "valence": np.float64,
        "tempo": np.float64,
        "type": str,
        "id": str,
        "uri": str,
        "track_href": str,
        "analysis_url": str,
        "duration_ms": "Int64",
        "time_signature": "Int64",
        "genre": str,
        "song_name": str,
        "Unnamed: 0": np.float64,
        "title": str,
    }
    genres_file_info = FileInfo(
        file_name="genres_v2.csv", sep=",", names=[], output_db=genres_output_db, dtype=genres_file_dtype,
    )
    songs_data_source = DataSource(
        url="https://www.kaggle.com/datasets/mrmorj/dataset-of-songs-in-spotify/data",
        source_name=DataSource.KAGGLE_DATA_SOURCE,
        files_info=[genres_file_info],
    )
    songs_pipeline = DataPipeline(data_source=songs_data_source)
    songs_pipeline.run_pipeline()
    
    twitter_output_db = OutputDBConfig(db_name="project.sqlite", table_name="tweets")
    twitter_file_dtype = {
        "clean_text": str,
        "category": "Int64",
    }
    twitter_file_info = FileInfo(
        file_name="Twitter_Data.csv", sep=",", names=[], output_db=twitter_output_db, dtype=twitter_file_dtype,
    )
    twitter_data_source = DataSource(
        url="https://www.kaggle.com/datasets/saurabhshahane/twitter-sentiment-dataset/",
        source_name=DataSource.KAGGLE_DATA_SOURCE,
        files_info=[twitter_file_info],
    )
    twitter_pipeline = DataPipeline(data_source=twitter_data_source)
    twitter_pipeline.run_pipeline()