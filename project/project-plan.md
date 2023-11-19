# Project Plan

## Title
Music Recommendation Based on Sentiment.

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Can we recommend music based on humand sentiment?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Music recommendation based on human sentiment is one of the interesting topics. Whitin this project's scope, I will be analysing the human sentiment based on the Social Network (Twitter post) and, Music data. And then suggesting music based on the mood.

First, social media post and music dataset will be collected from the datasources [Datasource1](#datasource1-twitter-dataset) and, 
[Datasource2](#datasource2-music-dataset) respectively. After that the texts of both the datasets will be analysed to score sentiments
with several methodologies. Few pre-trained models as well as libraries e.g NLTK can be used to score sentiments of both dataset.

Finally, music will be suggested based on the sentiment score from the social network post.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Twitter Dataset
* Metadata URL: http://help.sentiment140.com/for-students/
* Data URL: http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip
* Data Type: CSV

The data is a CSV with emoticons removed. Data file format has 6 fields:
* 0 - the polarity of the tweet (0 = negative, 2 = neutral, 4 = positive) (We will be calculating our own polarity and compare the score)
* 1 - the id of the tweet (2087)
* 2 - the date of the tweet (Sat May 16 23:58:44 UTC 2009)
* 3 - the query (lyx). If there is no query, then this value is NO_QUERY.
* 4 - the user that tweeted (robotickilldozr)
* 5 - the text of the tweet (Lyx is cool)

### Datasource1: Music Dataset
* Metadata URL: https://www.kaggle.com/datasets/mrmorj/dataset-of-songs-in-spotify/data
* Data URL: https://www.kaggle.com/datasets/mrmorj/dataset-of-songs-in-spotify/download?datasetVersionNumber=1
* Data Type: CSV

The full list of genres included in the CSV are Trap, Techno, Techhouse, Trance, Psytrance, Dark Trap, DnB (drums and bass), Hardstyle, Underground Rap, Trap Metal, Emo, Rap, RnB, Pop and Hiphop.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Investigate for interesting dataset [#1][i1]
2. Write initial Description about the project plan [#2][i2]
3. Construct ETL Pipeline [#3][i3]

[i1]: https://github.com/prantoamt/made-template/issues/1
[i2]: https://github.com/prantoamt/made-template/issues/2
[i3]: https://github.com/prantoamt/made-template/issues/8