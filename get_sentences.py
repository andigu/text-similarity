from sentence_preprocess import sentence_preprocess
from os import listdir


def fetch_corpus(corpus_directory):
    files = listdir(corpus_directory)
    for file in files:
        yield open(corpus_directory + "/" + file, "r")


def get_sentences():
    return get_corpus_sentences() + get_faq_sentences()

def get_corpus_sentences():
    sentences = []
    for file in fetch_corpus("C:\Andi\Programming\Algorithms\text_similarity\corpus\other"):
        try:
            sentences += [sentence_preprocess(file.read())]
        except UnicodeDecodeError:
            print(file.name)
    return sentences

def get_faq_sentences():
    sentences = [sentence_preprocess(open("corpus/home_page.txt", "r").read())] + \
                [sentence_preprocess(open("corpus/faq_4allseasons/" + str(i) + ".txt", "r").read()) for i in
                 range(1, 9)] + \
                [sentence_preprocess(open("corpus/faq_ezhome/" + str(i) + ".txt", "r").read()) for i in range(1, 39)] + \
                [sentence_preprocess(open("corpus/faq_rdpenner/" + str(i) + ".txt", "r").read()) for i in range(1, 5)] + \
                [sentence_preprocess(open("corpus/faq_myhealthylawn/" + str(i) + ".txt", "r").read()) for i in
                 range(1, 10)]
    return sentences
