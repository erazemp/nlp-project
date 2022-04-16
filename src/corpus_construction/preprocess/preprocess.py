import xml.etree.ElementTree as ET
import json
import os


def read_homonyms_file(filename):
    homonyms = []
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            homonyms.append(line.rstrip())
    return homonyms


def extract_sentences_from_corpus(directory, homonyms):
    homonyms_sentences = {}
    # TEMP
    i = 0
    for filename in os.listdir(directory):
        # TEMP for quick assessment
        i = i + 1
        if i > 5000:
            break
        # end TEMP
        print('parsing file ', filename)
        f = os.path.join(directory, filename)
        homonyms_sentences = extract_homonym_sentences(f, homonyms, homonyms_sentences)
    return homonyms_sentences


def extract_homonym_sentences(filename, homonyms, homonym_sentences):
    tree = ET.parse(filename)
    root = tree.getroot()
    for sentence_parsed in root.iter('{http://www.tei-c.org/ns/1.0}s'):
        # initialization of properties
        sentence = ''
        lemma_sentence = ''
        lemma = ''
        contains_homonym_lemma = False
        start_index = -1
        end_index = -1
        lemma_index = -1
        word_index = -1
        for word_xml in sentence_parsed:
            # if entry is not a word, skip it
            if not word_xml.text:
                continue
            # check if current word has a lemma
            if "lemma" in word_xml.attrib:
                word_index = word_index + 1
                # check if word lemma is a homonym
                if word_xml.attrib["lemma"] in homonyms:
                    lemma_index = word_index
                    contains_homonym_lemma = True
                    lemma = word_xml.attrib["lemma"]
                    # check if entry for this lemma already exists, if not, create one
                    if not word_xml.attrib["lemma"] in homonym_sentences.keys():
                        homonym_sentences[word_xml.attrib["lemma"]] = []
                    # calculate start and end index of lemma word in a sentence
                    start_index = len(sentence)
                    end_index = start_index + len(word_xml.text) - 1
                if lemma_sentence:
                    lemma_sentence = lemma_sentence + " "
                lemma_sentence = lemma_sentence + word_xml.attrib["lemma"]
            # don't add space at beginning of the sentence
            if sentence and not word_xml.text in (".", ",", "?", ":", "!"):
                sentence = sentence + " "
            # add current word to building sentence
            sentence = sentence + word_xml.text
        # if in this sentence we have a homonym lemma, add it to our list
        if contains_homonym_lemma:
            sentence_entry = SentenceEntry(sentence, lemma_sentence, start_index, end_index, lemma_index)
            homonym_sentences[lemma].append(sentence_entry)
    return homonym_sentences


def construct_output_temp(homonyms_sentences, json_filename, word_limit):
    outputs = []
    for word_in_question in homonyms_sentences:
        list_of_sentences = homonyms_sentences[word_in_question]
        number_of_inputs = 0
        # if an entry has more than 1 entry (sentence), we can construct a pair
        if len(list_of_sentences) > 1:
            for i, sentence1 in enumerate(list_of_sentences):
                for j, sentence2 in enumerate(list_of_sentences):
                    if number_of_inputs > word_limit:
                        break
                    if i <= j:
                        continue
                    output = OutputEntry(word_in_question, sentence1, sentence2)
                    outputs.append(output)
                    number_of_inputs = number_of_inputs + 1
    json_str = json.dumps([ot.__dict__ for ot in outputs])
    # save to JSON file
    with open(json_filename, "w") as outfile:
        outfile.write(json_str)


class OutputEntry:
    def __init__(self, word, sentence1_object, sentence2_object):
        self.word = word
        self.sentence1 = sentence1_object.sentence
        self.lemma_sentence1 = sentence1_object.lemma_sentence
        self.lemma_sentence2 = sentence2_object.lemma_sentence
        self.sentence2 = sentence2_object.sentence
        self.start1 = sentence1_object.start
        self.lemma_word_index1 = sentence1_object.lemma_word_index
        self.end1 = sentence1_object.end
        self.start2 = sentence2_object.start
        self.lemma_word_index2 = sentence2_object.lemma_word_index
        self.end2 = sentence2_object.end
        self.same_context = False


class SentenceEntry:
    def __init__(self, sentence, lemma_sentence, start, end, lemma_index):
        self.sentence = sentence
        self.lemma_sentence = lemma_sentence
        self.start = start
        self.end = end
        self.lemma_word_index = lemma_index


if __name__ == '__main__':
    gigafida_dirname = '../../../Gigafida_corpus'
    homonyms_filename = 'homonyms.txt'
    corpus_filename = 'corpus.json'
    word_limit = 10000000
    homonym = read_homonyms_file(homonyms_filename)
    homonyms_sentences = extract_sentences_from_corpus(gigafida_dirname, homonym)
    construct_output_temp(homonyms_sentences, corpus_filename, word_limit)
