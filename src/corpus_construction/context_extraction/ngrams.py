import json


def read_corpus(filename):
    # read JSON file created in preprocess step
    f = open(filename)
    data = json.load(f)
    f.close()
    return data


def construct_ngrams(pairs, n):
    ngrams = {}
    for pair in pairs:
        word = pair["word"]
        if word not in ngrams:
            ngrams[word] = {}


class NgramBuilder:
    def __init__(self, n):
        self.all_neighboring_words = {}
        self.n = n

    def process_sentence(self, lemma_sentence, start):
        words = lemma_sentence.split(" ")


def decide_same_context():
    pass


if __name__ == '__main__':
    corpus_file = '../preprocess/corpus.json'
    n = 2
    corpus_entries = read_corpus(corpus_file)
    construct_ngrams(corpus_entries, n)
