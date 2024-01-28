import urllib.request
import os
import pandas as pd
import sqlite3
from zipfile import ZipFile

# Download the ZIP file
url = 'https://gtfs.rhoenenergie-bus.de/GTFS.zip'
zip_file_path = 'data/GTFS.zip'
urllib.request.urlretrieve(url, zip_file_path)

# Extract and read the 'stops.txt' file
with ZipFile(zip_file_path, 'r') as zip_ref:
    with zip_ref.open('stops.txt') as stops_file:
        # Reading the file into a pandas DataFrame
        stops_df = pd.read_csv(stops_file)

# Filtering data for zone 2001 and selecting required columns
selected_columns = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id']
stops_data = stops_df[stops_df['zone_id'] == 2001][selected_columns]

# Validating latitude and longitude
stops_data = stops_data[(stops_data['stop_lat'].between(-90, 90)) & 
                        (stops_data['stop_lon'].between(-90, 90))]

# Removing rows with missing or invalid data
stops_data.dropna(inplace=True)

# Path for the SQLite database
db_path = 'gtfs.sqlite'

# Creating and connecting to the SQLite database
conn = sqlite3.connect(db_path)

# Writing the data into the database
stops_data.to_sql('stops', conn, if_exists='replace', index=False, dtype={
    'stop_id': 'INTEGER',
    'stop_name': 'TEXT',
    'stop_lat': 'REAL',
    'stop_lon': 'REAL',
    'zone_id': 'INTEGER'
})

# Closing the database connection
conn.close()

# Delete the ZIP file
os.remove(zip_file_path)