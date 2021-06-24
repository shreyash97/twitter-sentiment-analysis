import nltk


def toToken(str):
    str = nltk.word_tokenize(str)
    print(str)
