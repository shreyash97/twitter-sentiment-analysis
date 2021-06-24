from nltk import tokenize
import db_conn
import word_list
import nltk


def process(queryTerm):
    mydatabase = db_conn.db
    clean_data_coll = db_conn.clean_data_collection
    queryTerm = queryTerm.lower()
    cursor = clean_data_coll.find({'keyword': queryTerm})

    posList = word_list.pos_list_func()
    negList = word_list.neg_list_func()

    for record in cursor:
        tokenText = nltk.word_tokenize(record['text'])
        posWords = []
        negWords = []
        posCount = 0
        negCount = 0
        for item in tokenText:
            if item in posList:
                posWords.append(item)
                posCount += 1
            elif item in negList:
                negWords.append(item)
                negCount += 1

        if negCount > posCount:
            sentiment = 'Negative'
        elif posCount > negCount:
            sentiment = 'Positive'
        else:
            sentiment = 'Neutral'

        rec = {'keyword': queryTerm, 'originalTweet': record['originalTweet'], 'text': record['text'], 'pos_word_count': posCount,
               'neg_word_count': negCount, 'positive_words': posWords, 'negative_words': negWords, 'sentiment': sentiment}

        result = mydatabase.processed_data.insert_one(rec)
