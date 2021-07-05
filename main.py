from typing import final
import fetch_tweets
import clean_tweets
import process
import db_conn
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/<queryTerm>/<int:count>")
def analyse(queryTerm, count):
    fetch_tweets.fetch_tweets(queryTerm, count)
    clean_tweets.clean_tweets(queryTerm)
    process.process(queryTerm)

    db = db_conn.db
    processed_data_collection = db_conn.processed_data_collection

    cursor = processed_data_collection.find({'keyword': queryTerm})
    neg_count = 0
    pos_count = 0
    neu_count = 0
    totalposwordList = []
    finalposwordList = []
    totalnegwords = []
    finalnegwordList = []

    for record in cursor:
        positive_word_list = list(record['positive_words'])
        negative_word_list = list(record['negative_words'])
        for i in positive_word_list:
            totalposwordList.append(i)
        for i in negative_word_list:
            totalnegwords.append(i)
        sentiment = record['sentiment']
        sentiment = sentiment.lower()
        if sentiment == 'negative':
            neg_count += 1
        elif sentiment == 'positive':
            pos_count += 1
        else:
            neu_count += 1
    for word in totalposwordList:
        countElem = totalposwordList.count(word)
        temp = {'value': word, "count": countElem}
        if temp not in finalposwordList:
            finalposwordList.append(temp)

    for word in totalnegwords:
        countNegElem = totalnegwords.count(word)
        pair = {'value': word, 'count': countNegElem}
        if pair not in finalnegwordList:
            finalnegwordList.append(pair)

    # tempList = list(set(finalposwordList))
    res = {'Keyword': queryTerm, 'pos': pos_count,
           'neg': neg_count, 'neu': neu_count, 'positiveList': finalposwordList, 'negativeList': finalnegwordList}
    result = jsonify(res)
    result.headers.add('Access-Control-Allow-Origin', '*')

    return result


if __name__ == '__main__':
    app.run(debug=True)
