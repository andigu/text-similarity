# Model 1: just faq and answers to those
# Model 2: model 1 + other gardening websites
# Model 3: model 2 + literature, etc much larger corpus
# Model 4: model 3, but much more training on gardening vs other corpus (increased weighting on gardening stuff) 500 to 50


import logging
from gensim.models import Word2Vec
from get_sentences import *

global sentences

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model_location = "model/model_4"
try:
    model = Word2Vec.load(model_location)
except FileNotFoundError:
    model = Word2Vec()
    sentences = get_sentences()
    model.build_vocab(sentences)

faq = get_faq_sentences()
for i in range(500):
    if i % 100 == 0:
        print(i)
    model.train(faq)
print("done faq")
corpus = get_corpus_sentences()
for i in range(100):
    if i % 10 == 0:
        print(i)
    model.train(corpus)
model.save(model_location)
