# Project Plan

## Title
Music Recommendation Based on human mood.

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
* Metadata URL: https://www.kaggle.com/datasets/edenbd/150k-lyrics-labeled-with-spotify-valence
* Data URL: https://www.kaggle.com/datasets/edenbd/150k-lyrics-labeled-with-spotify-valence
* Data Type: ZIP

The URL will return a ZIP file containing 1 file: "labeled_lyrics_cleaned.csv".
There are total 1,58,353 unique song lyrics in "labeled_lyrics_cleaned.csv" and 5 Columns :

|       Column number     |      Column Name        |      Description        |
|-------------------------|-------------------------|-------------------------|
|             0           |      #                  |      Song number        |
|             1           |      artist             |      Artist name        |
|             2           |      seq                |      Song's lyrics      |
|             3           |      song               |      Song title         |
|             4           |      label              |      Spotify valence (Positiveness) feature attribute for this song |


## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Investigate for interesting dataset [#1][i1]
2. Write initial Description about the project plan [#2][i2]
3. Construct ETL Pipeline [#3][i3]
4. Create test cases for ETL Pipeline [#4][i4]
4. Explore data for model training and predictions [#5][i5]

[i1]: https://github.com/prantoamt/made-template/issues/1
[i2]: https://github.com/prantoamt/made-template/issues/2
[i3]: https://github.com/prantoamt/made-template/issues/8
[i4]: https://github.com/prantoamt/made-template/issues/15
[i5]: https://github.com/prantoamt/made-template/issues/16