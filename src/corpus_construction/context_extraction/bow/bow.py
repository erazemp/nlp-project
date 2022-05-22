import string
from string import digits
import json
import scipy.spatial

from evaluate import perform_evaluation


# UTILS methods
def read_json_file(filename):
    # read JSON file created in preprocess step
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def read_json_files_and_combine_them(filenames, base_path):
    combined = []
    for filename in filenames:
        path = base_path + filename + '.json'
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            combined.extend(data)
    return combined


def save_json_file(pairs, json_filename):
    print('Saving to JSON file')
    json_str = json.dumps([p for p in pairs], indent=2, ensure_ascii=False)
    # save to JSON file
    with open(json_filename, "w", encoding='utf-8') as outfile:
        outfile.write(json_str)


def save_part_of_data_for_evaluation(pairs, json_filename, num_of_each_instance):
    # save part of corpus into another json file for manual annotation / validation
    print('Saving part of data')
    temp = {}
    part_corpus = []
    for pair in pairs:
        target_word = pair["word"]
        if target_word not in temp:
            temp[target_word] = [0, 0]
        if temp[target_word][0] == num_of_each_instance and temp[target_word][1] == num_of_each_instance:
            continue
        if pair["same_context"] and temp[target_word][0] < num_of_each_instance:
            temp[target_word][0] = temp[target_word][0] + 1
            part_corpus.append(pair)
        elif not pair["same_context"] and temp[target_word][1] < num_of_each_instance:
            temp[target_word][1] = temp[target_word][1] + 1
            part_corpus.append(pair)
    json_str = json.dumps([p for p in part_corpus], indent=2, ensure_ascii=False)
    with open(json_filename, "w", encoding='utf-8') as outfile:
        outfile.write(json_str)


def construct_bow(pairs, window):
    bow_builder = BowBuilder(window)
    # iterate through all the sentences to get context vectors
    print('Constructing bow')
    for pair in pairs:
        word = pair["word"]
        bow_builder.construct_neighbouring_vector(pair["lemma_sentence1"], word, pair["lemma_word_index1"])
        bow_builder.construct_neighbouring_vector(pair["lemma_sentence2"], word, pair["lemma_word_index2"])
    return bow_builder


def fill_vectors(bow_builder, pairs, cosine_distance_threshold):
    print('Filling vectors')
    for pair in pairs:
        word = pair["word"]
        context_vector1 = bow_builder.count_occurrences(pair["lemma_sentence1"], word, pair["lemma_word_index1"])
        context_vector2 = bow_builder.count_occurrences(pair["lemma_sentence2"], word, pair["lemma_word_index2"])
        distance = calculate_cosine_similarity(context_vector1, context_vector2)
        if distance > cosine_distance_threshold:
            pair["same_context"] = True
    return pairs


def calculate_cosine_similarity(vector1, vector2):
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
        # if word is at beginning or end of sentence, prevent out of bounds
        if start < 0:
            start = 0
        end = index + self.n + 1
        if end > len(words):
            end = len(words)
        return words[start:end]


if __name__ == '__main__':
    homonyms = ['klop', 'list', 'postaviti', 'prst', 'surov', 'tema', 'tip', 'vila']
    validated_corpus_location = '../../validated_corpus/'
    # data_file = '../../preprocess/preprocessed_data.json'
    results_file = 'bow_corpus.json'
    part_results_file = 'bow_corpus_part.json'
    window_size = 2
    cosine_distance_threshold = 0.7
    # corpus_entries = read_json_file(data_file)
    corpus_entries = read_json_files_and_combine_them(homonyms, validated_corpus_location)
    bow = construct_bow(corpus_entries, window_size)
    updated_pairs = fill_vectors(bow, corpus_entries, cosine_distance_threshold)
    save_json_file(updated_pairs, results_file)
    # save_part_of_data_for_evaluation(updated_pairs, part_results_file, 50)
    perform_evaluation(False, validated_corpus_location, updated_pairs, homonyms)
