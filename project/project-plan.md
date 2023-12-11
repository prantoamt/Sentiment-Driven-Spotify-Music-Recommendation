# Project Plan

## Title
Sentiment-Driven Spotify Music Recommendation: Leveraging Social Media Posts and User Playlists for Personalized Music Experiences

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. How does logistic regression performs on sentiment classification?
2. Can we use transfer learning to classify sentiments on music lyrics?
3. Can we suggest music based on the sentiment of social media post?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Music recommendation based on human sentiment is one of the interesting topics. Whitin this project's scope, I will be analysing the human sentiment based on the Social Network (Twitter post) and, Music data. And then suggesting music based on the mood.

First, social media post and music dataset will be collected from the datasources [Datasource1](#datasource1-twitter-dataset) and, 
[Datasource2](#datasource2-music-dataset) respectively. After that the texts of both the datasets will be analysed to score sentiments
with several methodologies.

Finally, music will be suggested based on the sentiment score from the social network post.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Twitter Dataset
* Metadata URL: https://www.kaggle.com/datasets/kazanova/sentiment140
* Data URL: https://www.kaggle.com/datasets/kazanova/sentiment140
* Data Type: ZIP

The URL will return a ZIP file containing 1 file: "training.1600000.processed.noemoticon.csv". There are total 1.6 million tweets from several users and 6 columns.

|       Column number     |      Column Name        |      Description        |
|-------------------------|-------------------------|-------------------------|
|             0           |      target             |      Sentiment          |
|             1           |      id                 |      Tweet id           |
|             2           |      date               |      Tweet date         |
|             3           |      flag               |      N/A                |
|             4           |      user               |      User               |
|             5           |      text               |      Tweet              |

### Datasource2: Music Dataset
* Metadata URL: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023
* Data URL: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023
* Data Type: ZIP

|       Column number                 |                    Column Name        |                                  Description        |
|-------------------------------------|---------------------------------------|-----------------------------------------------------|
|             0                       |        track_name                     |      Name of the song.                              |   
|             1                       |        artist(s)_name                 |      Name of the artist(s) of the song.             |
|             2                       |        artist_count                   |      Number of artists contributing to the song.    |
|             3                       |        released_year                  |      Year when the song was released.               |
|             4                       |        released_month                 |      Month when the song was released.              |
|             5                       |        released_day                   |      Day of the month when the song was released.   |
|             6                       |        in_spotify_playlists           |      Number of Spotify playlists the song is included in. |
|             7                       |        in_spotify_charts              |      Presence and rank of the song on Spotify charts. |
|             8                       |        streams                        |      Total number of streams on Spotify.             |
|             9                       |        in_apple_playlists             |      Number of Apple Music playlists the song is included in. |
|             10                      |        in_apple_charts                |      Presence and rank of the song on Apple Music charts. |
|             11                      |        in_deezer_playlists            |      Number of Deezer playlists the song is included in. |
|             12                      |        in_deezer_charts               |      Presence and rank of the song on Deezer charts. |
|             13                      |        in_shazam_charts               |      Presence and rank of the song on Shazam charts. |
|             14                      |        bpm                            |      Beats per minute, a measure of song tempo.      |
|             15                      |        key                            |      Key of the song.                                |
|             16                      |        mode                           |      Mode of the song (major or minor).              |
|             17                      |        danceability_%                 |      Percentage indicating how suitable the song is for dancing. |
|             18                      |        valence_%                      |      Positivity of the song's musical content.       |
|             19                      |        energy_%                       |      Perceived energy level of the song.             |
|             20                      |        acousticness_%                 |      Amount of acoustic sound in the song.           |
|             21                      |        instrumentalness_%             |      Amount of instrumental content in the song.     |
|             22                      |        liveness_%                     |      Presence of live performance elements.          |
|             23                      |        speechiness_%                  |      Amount of spoken words in the song.             |

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Investigate for interesting dataset. [#1][i1]
2. Write initial Description about the project plan. [#2][i2]
3. Construct ETL Pipeline. [#3][i3]
4. Create test cases for ETL Pipeline. [#4][i4]
4. Explore data for model training and predictions. [#5][i5]
4. Write final report. [#5][i5]

[i1]: https://github.com/prantoamt/made-template/issues/1
[i2]: https://github.com/prantoamt/made-template/issues/2
[i3]: https://github.com/prantoamt/made-template/issues/8
[i4]: https://github.com/prantoamt/made-template/issues/15
[i5]: https://github.com/prantoamt/made-template/issues/16
[i6]: https://github.com/prantoamt/made-template/issues/31