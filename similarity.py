import operator
import numpy as np
from gensim.models import Word2Vec
from sentence_preprocess import sentence_preprocess


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    if v1 is not None and v2 is not None:
        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def average_vectors(vectors):
    return sum(vectors) / len(vectors)


def average_sentence_vector(sentence, model):
    return average_vectors([model[word] for word in sentence])


version = 4
model = Word2Vec.load("model/model_" + str(version))
raw = input()
query = sentence_preprocess(raw)
while len(query) == 0:
    print("query too short, reenter")
    raw = input()
    query = sentence_preprocess(raw)

file = open("history_" + str(version) + ".txt", "a")
while raw != "stop":
    similarities = {}
    for line in open("questions.txt", "r"):
        line = line.replace("\n", "")
        similarities[line] = angle_between(average_sentence_vector(sentence_preprocess(line), model),
                                           average_sentence_vector(query, model))
    sorted_x = sorted(similarities.items(), key=operator.itemgetter(1), reverse=False)[:3]
    file.write(raw + "\n")
    for i in sorted_x:
        file.write(str(i) + "\n")
        print(i)
    raw = input()
    query = sentence_preprocess(raw)
    while len(query) == 0:
        print("query too short, reenter")
        raw = input()
        query = sentence_preprocess(raw)
file.flush()
file.close()
