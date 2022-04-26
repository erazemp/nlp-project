import json
import string
from string import digits

import scipy.spatial


def clean_text(corpus_entries):
    for entry in corpus_entries:
        # print(entry['sentence1'])
        entry['sentence1'] = entry['sentence1'].lower().translate(str.maketrans('', '', string.punctuation))
        entry['sentence1'] = entry['sentence1'].translate(str.maketrans('', '', digits))
        entry['lemma_sentence1'] = entry['lemma_sentence1'].lower().translate(str.maketrans('', '', string.punctuation))
        entry['lemma_sentence1'] = entry['lemma_sentence1'].lower().translate(str.maketrans('', '', digits))
        entry['lemma_sentence2'] = entry['lemma_sentence2'].lower().translate(str.maketrans('', '', string.punctuation))
        entry['lemma_sentence2'] = entry['lemma_sentence2'].translate(str.maketrans('', '', digits))
        entry['sentence2'] = entry['sentence2'].lower().translate(str.maketrans('', '', string.punctuation))
        entry['sentence2'] = entry['sentence2'].translate(str.maketrans('', '', digits))
        # print(entry['sentence1'])


def read_corpus(filename):
    # read JSON file created in preprocess step
    f = open(filename)
    data = json.load(f)
    f.close()
    return data


def construct_bow(pairs, window):
    bow_builder = BowBuilder(window)
    # iterate through all the sentences to get context vectors
    for pair in pairs:
        word = pair["word"]
        bow_builder.construct_neighbouring_vector(pair["lemma_sentence1"], word, pair["lemma_word_index1"])
        bow_builder.construct_neighbouring_vector(pair["lemma_sentence2"], word, pair["lemma_word_index2"])
    return bow_builder


def fill_vectors(bow_builder, pairs, cosine_distance_threshold):
    for pair in pairs:
        word = pair["word"]
        context_vector1 = bow_builder.count_occurrences(pair["lemma_sentence1"], word, pair["lemma_word_index1"])
        context_vector2 = bow_builder.count_occurrences(pair["lemma_sentence2"], word, pair["lemma_word_index2"])
        distance = calculate_cosine_distance(context_vector1, context_vector2)
        if distance > cosine_distance_threshold:
            pair["same_context"] = True
    return pairs


def save_json_file(pairs, json_filename):
    json_str = json.dumps([p for p in pairs])
    # save to JSON file
    with open(json_filename, "w") as outfile:
        outfile.write(json_str)


def calculate_cosine_distance(vector1, vector2):
    v1 = []
    v2 = []
    for word in vector1.keys():
        v1.append(vector1[word])
        v2.append(vector2[word])
    return 1 - scipy.spatial.distance.cosine(v1, v2)


class BowBuilder:
    def __init__(self, n):
        self.lemma_neighboring_words = {}
        self.n = n

    def construct_neighbouring_vector(self, lemma_sentence, lemma, index):
        if lemma not in self.lemma_neighboring_words:
            self.lemma_neighboring_words[lemma] = {}
        neighbouring_words = self.get_neighboring_words(lemma_sentence, index)
        for neighbouring_word in neighbouring_words:
            # don't include lemma as it is always present
            if neighbouring_word == lemma:
                continue
            if neighbouring_word not in self.lemma_neighboring_words[lemma]:
                self.lemma_neighboring_words[lemma][neighbouring_word] = 0

    def count_occurrences(self, lemma_sentence, lemma, index):
        neighbouring_words = self.get_neighboring_words(lemma_sentence, index)
        context_vector = self.lemma_neighboring_words[lemma].copy()
        for neighbouring_word in neighbouring_words:
            # don't include lemma as it is always present
            if neighbouring_word == lemma:
                continue
            context_vector[neighbouring_word] = context_vector[neighbouring_word] + 1
        return context_vector

    def get_neighboring_words(self, lemma_sentence, index):
        words = lemma_sentence.split(" ")
        start = index - self.n
        if start < 0:
            start = 0
        end = index + self.n + 1
        if end > len(words):
            end = len(words)
        return words[start:end]


if __name__ == '__main__':
    corpus_file = '../../preprocess/corpus.json'
    window_size = 2
    corpus_entries = read_corpus(corpus_file)
    # clean_text(corpus_entries)
    #remove_stop_words(corpus_entries)
    bow = construct_bow(corpus_entries, window_size)
    #remove_stop_words(bow)
    updated_pairs = fill_vectors(bow, corpus_entries, 0.7)
    save_json_file(updated_pairs, 'new_corpus.json')
    print("done")
