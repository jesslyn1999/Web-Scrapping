from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import os

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stopwords = ''


def stem_id(words):
    if isinstance(words, (list, tuple, set)):
        return [stemmer.stem(word) for word in words]
    else:  # just a word
        return stemmer.stem(words)


def get_stopwords(relative_path='res/stopword.txt'):
    global stopwords
    if not stopwords:
        with open(os.path.abspath(relative_path)) as in_f:
            stopwords = [line.rstrip('\n') for line in in_f]
    return stopwords


