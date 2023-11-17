# Python imports

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
    genres_file_info = FileInfo(
        file_name="genres_v2.csv", sep=",", names=[], output_db=genres_output_db
    )
    songs_data_source = DataSource(
        url="https://www.kaggle.com/datasets/mrmorj/dataset-of-songs-in-spotify/data",
        source_name="kaggle",
        files_info=[genres_file_info],
    )
    songs_pipeline = DataPipeline(data_source=songs_data_source)
    songs_pipeline.run_pipeline()
