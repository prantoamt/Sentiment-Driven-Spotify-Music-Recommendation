# Python import
import re

# Third-party imports
from nltk import download as nltkdownload
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Self imports
from project.pipeline import construct_twitter_pipeline


class TestTransform:
    def test_tweet_transform(self, mock_tweet_df):
        preprocessed_tweet = (
            construct_twitter_pipeline()
            .extractor.file_handlers[0]
            .transformer(mock_tweet_df)
        )
        assert preprocessed_tweet.shape == (2, 3)
        assert list(preprocessed_tweet.columns.values) == [
            "target",
            "text",
            "processed_text",
        ]
        assert preprocessed_tweet.iloc[0]["target"] == 0
        assert preprocessed_tweet.iloc[1]["target"] == 1
        print(preprocessed_tweet.iloc[1]["processed_text"])
        assert (
            preprocessed_tweet.iloc[0]["processed_text"]
            == "mock tweet target contains one tag one link several special character exmaple"
        )
        assert (
            preprocessed_tweet.iloc[1]["processed_text"]
            == "another mock tweet target contains one tag one link several special character exmaple"
        )
