
neg_file = open(
    "/Users/vertigo/Desktop/Twitter ANalysis/opinion-lexicon-English/negative-words.txt", encoding="ISO-8859-1")
pos_file = open(
    "/Users/vertigo/Desktop/Twitter ANalysis/opinion-lexicon-English/positive-words.txt")

pos_list = []
neg_list = []


def pos_list_func():
    for word in pos_file:
        word = word.rstrip("\n")
        pos_list.append(word)
    return pos_list


def neg_list_func():
    for word in neg_file:
        word = word.rstrip("\n")
        neg_list.append(word)
    return neg_list


# neg_file.close()
# pos_file.close()
