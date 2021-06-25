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

    for record in cursor:

        sentiment = record['sentiment']
        sentiment = sentiment.lower()
        if sentiment == 'negative':
            neg_count += 1
        elif sentiment == 'positive':
            pos_count += 1
        else:
            neu_count += 1
    result = {'Keyword': queryTerm, 'Total Positive Tweets': pos_count,
              'Total Negative Tweets': neg_count, 'Total Neutral Tweets': neu_count}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
