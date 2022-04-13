import xml.etree.ElementTree as ET
import json


def read_file(filename, words):
    tree = ET.parse(filename)
    root = tree.getroot()
    sentences = {}
    for sentence_xml in root.iter('{http://www.tei-c.org/ns/1.0}s'):
        sentence = ''
        lemma = ''
        include = False
        for word in sentence_xml:
            if not word.text:
                continue
            if "lemma" in word.attrib and word.attrib["lemma"] in words:
                include = True
                lemma = word.attrib["lemma"]
                if not word.attrib["lemma"] in sentences.keys():
                    sentences[word.attrib["lemma"]] = []
            # don't add space at beginning of the sentence
            if sentence and not word.text in (".", ",", "?", ":", "!"):
                sentence = sentence + " "
            sentence = sentence + word.text
        if include:
            sentences[lemma].append(sentence)
    return sentences


def construct_output_temp(sentences):
    outputs = []
    for word_in_question in sentences:
        list_of_sentences = sentences[word_in_question]
        if len(list_of_sentences) > 1:
            output = OutputEntry(word_in_question)
            output.with_sentence1(list_of_sentences[0], -2, -2)
            output.with_sentence2(list_of_sentences[1], -2, -2)
            outputs.append(output)
    json_str = json.dumps([ob.__dict__ for ob in outputs])
    print(json_str)


class OutputEntry:
    def __init__(self, word):
        self.word = word
        self.sentence1 = ""
        self.sentence2 = ""
        self.start1 = -1
        self.end1 = -1
        self.start2 = -1
        self.end2 = -1
        self.same_context = False

    def with_sentence1(self, sentence, start, end):
        self.sentence1 = sentence
        self.start1 = start
        self.end1 = end

    def with_sentence2(self, sentence, start, end):
        self.sentence2 = sentence
        self.start2 = start
        self.end2 = end


if __name__ == '__main__':
    filename = '../../../Gigafida_corpus/F0000008.xml'
    words = ('letos', 'shraniti')
    sentences = read_file(filename, words)
    # print(sentences)
    construct_output_temp(sentences)


