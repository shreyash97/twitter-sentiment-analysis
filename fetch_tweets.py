import tweepy
import db_conn
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def fetch_tweets(queryTerm, tweetNum):

    mydatabase = db_conn.db
    mycollection = db_conn.raw_data_collection

    consumer_key = os.environ.get('consumer_key')
    consumer_secret = os.environ.get('consumer_secret')
    access_token = os.environ.get('access_token')
    access_token_secret = os.environ.get('access_token_secret')
    bearer_token = os.environ.get('bearer_token')

    auth = tweepy.OAuthHandler(consumer_key,
                               consumer_secret)
    auth.set_access_token(access_token,
                          access_token_secret)

    api = tweepy.API(auth)
    queryTerm = str(queryTerm).lower()
    for tweet in tweepy.Cursor(api.search_tweets, tweet_mode='extended', lang='en', result_type="recent", q=queryTerm).items(tweetNum):

        try:
            rec = {'keyword': queryTerm,
                   'text': tweet.retweeted_status.full_text}
            result = mydatabase.raw_data.insert_one(rec)

        except AttributeError:  # Not a Retweet

            rec = {'keyword': queryTerm,
                   'text': tweet.full_text}
            result = mydatabase.raw_data.insert_one(rec)
