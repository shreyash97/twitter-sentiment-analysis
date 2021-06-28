import re
import string
from threading import current_thread
import db_conn
import nltk
from nltk.corpus import stopwords


def clean_tweets(queryTerm):

    mydatabase = db_conn.db
    raw_data_collection = db_conn.raw_data_collection
    stop_words = stopwords.words("english")
    queryTerm = queryTerm.lower()

    cursor = raw_data_collection.find({'keyword': queryTerm})

    for record in cursor:
        str = record['text'].lower()
        str = str.encode('ascii', 'ignore').decode()  # remove Unicode chars
        str = ' '.join([word for word in str.split(
            ' ') if word not in stop_words])  # remove stop words
        str = re.sub("@\S+", " ", str)  # Removes mentions
        str = re.sub("https*\S+", " ", str)  # removes urls
        str = re.sub("#\S+", " ", str)  # remove hashtags
        str = re.sub('[%s]' % re.escape(string.punctuation),
                     ' ', str)  # Removes punctuations
        str = re.sub(r'\w*\d+\w*', '', str)  # remove numbers
        str.strip()

        rec = {'keyword': queryTerm,
               'originalTweet': record['text'],
               'text': str}

        result = mydatabase.clean_data.insert_one(rec)
