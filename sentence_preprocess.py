import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def sentence_preprocess(sentence):
    return remove_stop_words(remove_grammar(sentence))


def remove_stop_words(sentence):
    stemmer = PorterStemmer()
    to_remove = stopwords.words('english') + ["ezhome", "ezhomes"]
    return [stemmer.stem(word) for word in re.findall(r"[\w']+", sentence) if word not in to_remove]


def remove_grammar(sentence):
    return sentence.lower().replace(",", "").replace("'", "").replace('"', "")
