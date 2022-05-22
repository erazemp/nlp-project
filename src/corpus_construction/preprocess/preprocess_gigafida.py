import string
import xml.etree.ElementTree as ET
import json
import os

stop_words = ["a", "ali", "april", "avgust", "b", "bi", "bil", "bila", "bile", "bili", "bilo", "biti", "blizu",
              "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boš", "brez", "c", "cel", "cela",
              "celi", "celo", "d", "da", "daleč", "dan", "danes", "datum", "december", "deset", "deseta", "deseti",
              "deseto", "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler",
              "dol", "dolg", "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e",
              "eden", "en", "ena", "ene", "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.",
              "gor", "gospa", "gospod", "h", "halo", "i", "idr.", "ii", "iii", "in", "iv", "ix", "iz", "j",
              "januar", "jaz", "je", "ji", "jih", "jim", "jo", "julij", "junij", "jutri", "k", "kadarkoli", "kaj",
              "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar", "karkoli", "katerikoli", "kdaj", "kdo",
              "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder", "koderkoli", "koga", "komu", "kot",
              "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki", "lahko", "le", "lep", "lepa",
              "lepe", "lepi", "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni", "malce", "malo", "manj",
              "marec", "me", "med", "medtem", "mene", "mesec", "mi", "midva", "midve", "mnogo", "moj", "moja",
              "moje", "mora", "morajo", "moram", "moramo", "morate", "moraš", "morem", "mu", "n", "na", "nad",
              "naj", "najina", "najino", "najmanj", "naju", "največ", "nam", "narobe", "nas", "nato", "nazaj",
              "naš", "naša", "naše", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri",
              "nekatero", "nekdo", "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoč", "ni", "nikamor",
              "nikdar", "nikjer", "nikoli", "nič", "nje", "njega", "njegov", "njegova", "njegovo", "njej", "njemu",
              "njen", "njena", "njeno", "nji", "njih", "njihov", "njihova", "njihovo", "njiju", "njim", "njo",
              "njun", "njuna", "njuno", "no", "nocoj", "november", "npr.", "o", "ob", "oba", "obe", "oboje", "od",
              "odprt", "odprta", "odprti", "okoli", "oktober", "on", "onadva", "one", "oni", "onidve", "osem",
              "osma", "osmi", "osmo", "oz.", "p", "pa", "pet", "peta", "petek", "peti", "peto", "po", "pod",
              "pogosto", "poleg", "poln", "polna", "polni", "polno", "ponavadi", "ponedeljek", "ponovno", "potem",
              "povsod", "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi", "pravo", "prazen",
              "prazna", "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.", "približno",
              "primer", "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r",
              "ravno", "redko", "res", "reč", "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe",
              "sebi", "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si", "sicer",
              "skoraj", "skozi", "slab", "smo", "so", "sobota", "spet", "sreda", "srednja", "srednji", "sta", "ste",
              "stran", "stvar", "sva", "t", "ta", "tak", "taka", "take", "taki", "tako", "takoj", "tam", "te",
              "tebe", "tebi", "tega", "težak", "težka", "težki", "težko", "ti", "tista", "tiste", "tisti", "tisto",
              "tj.", "tja", "to", "toda", "torek", "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj",
              "tvoj", "tvoja", "tvoje", "u", "v", "vaju", "vam", "vas", "vaš", "vaša", "vaše", "ve", "vedno",
              "velik", "velika", "veliki", "veliko", "vendar", "ves", "več", "vi", "vidva", "vii", "viii", "visok",
              "visoka", "visoke", "visoki", "vsa", "vsaj", "vsak", "vsaka", "vsakdo", "vsake", "vsaki", "vsakomur",
              "vse", "vsega", "vsi", "vso", "včasih", "včeraj", "x", "z", "za", "zadaj", "zadnji", "zakaj",
              "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "č", "če", "često", "četrta", "četrtek",
              "četrti", "četrto", "čez", "čigav", "š", "šest", "šesta", "šesti", "šesto", "štiri", "ž", "že"]


def stop_word_check(word):
    word = word.lower()
    split_word = list(word)
    for el in split_word:
        if el in list(string.punctuation) or el == "»" or el == "«":
            return False
    if any(char.isdigit() for char in word):
        return False
    if word.isnumeric() or word in list(string.punctuation) or word in stop_words:
        return False
    return True


def extract_sentences_from_corpus(directory, homonyms, c1, c2, stop_word_check=True):
    global stop_words
    if not stop_word_check:
        stop_words = []

    homonyms_sentences = {}
    # TEMP
    i = 0
    for filename in os.listdir(directory):
        # only process 10000 corpus files
        i = i + 1
        if i > 10000:
            break
        # end TEMP
        print('parsing file ', filename)
        f = os.path.join(directory, filename)
        homonyms_sentences, c1, c2 = extract_homonym_sentences(f, homonyms, homonyms_sentences, c1, c2)
        a = 0
    print("counts: ", c1, c2)
    return homonyms_sentences


def extract_homonym_sentences(filename, homonyms, homonym_sentences, count, count2):
    tree = ET.parse(filename)
    root = tree.getroot()
    for sentence_xml_element in root.iter('{http://www.tei-c.org/ns/1.0}s'):
        # initialization of properties
        sentence_entry = SentenceObject()
        lemma = ''
        contains_homonym_lemma = False
        target_word_index = -1
        for xml_element in sentence_xml_element:
            # if entry is not a word, skip it
            if not xml_element.text:
                continue
            # check if word is a stop word or number:
            current_word = xml_element.text
            count2 += 1
            if not stop_word_check(current_word):
                count += 1
                continue
            if "lemma" in xml_element.attrib:
                if not stop_word_check(xml_element.attrib["lemma"]):
                    count += 1
                    continue
            # check if current word has a lemma (is of type word)
            if xml_element.tag == '{http://www.tei-c.org/ns/1.0}w':
                target_word_index = target_word_index + 1
                # check if word lemma is a homonym
                if xml_element.attrib["lemma"] in homonyms:
                    sentence_entry.lemma_word_index = target_word_index
                    contains_homonym_lemma = True
                    lemma = xml_element.attrib["lemma"]
                    # check if entry for this lemma already exists, if not, create one
                    if not xml_element.attrib["lemma"] in homonym_sentences.keys():
                        homonym_sentences[xml_element.attrib["lemma"]] = []
                    # calculate start and end index of lemma word in a sentence
                    sentence_entry.start = len(sentence_entry.sentence)
                    sentence_entry.end = sentence_entry.start + len(current_word) - 1
                if sentence_entry.lemma_sentence:
                    sentence_entry.lemma_sentence = sentence_entry.lemma_sentence + " "
                sentence_entry.lemma_sentence = sentence_entry.lemma_sentence + xml_element.attrib["lemma"]
                if sentence_entry.sentence:
                    sentence_entry.sentence = sentence_entry.sentence + " "
            # add current word to building sentence
            sentence_entry.sentence = sentence_entry.sentence + current_word
        # if in this sentence we have a homonym lemma, add it to our list
        if contains_homonym_lemma:
            homonym_sentences[lemma].append(sentence_entry)
    return homonym_sentences, count, count2


def construct_output_temp(homonyms_sentences, json_filename, word_limit):
    outputs = []
    for word_in_question in homonyms_sentences:
        list_of_sentences = homonyms_sentences[word_in_question]
        number_of_inputs = 0
        # if an entry has more than 1 entry (sentence), we can construct a pair
        if len(list_of_sentences) > 1:
            for i in range(0, len(list_of_sentences) - 1, 2):
                sentence1 = list_of_sentences[i]
                sentence2 = list_of_sentences[i + 1]
                if number_of_inputs > word_limit:
                    break
                output = OutputEntry(word_in_question, sentence1, sentence2)
                outputs.append(output)
                number_of_inputs = number_of_inputs + 1
    json_str = json.dumps([ot.__dict__ for ot in outputs], indent=2, ensure_ascii=False)
    # save to JSON file
    with open(json_filename, "w", encoding='utf-8') as outfile:
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


class SentenceObject:
    def __init__(self):
        self.sentence = ''
        self.lemma_sentence = ''
        self.start = -1
        self.end = -1
        self.lemma_word_index = -1


if __name__ == '__main__':
    gigafida_dirname = '../../../Gigafida_corpus'
    homonyms_filename = 'homonyms.txt'
    corpus_filename = 'preprocessed_data.json'
    # TEMP parameter to limit how many
    word_limit = 10000000
    homonyms = ['klop', 'list', 'postaviti', 'prst', 'surov', 'tema', 'tip']
    c1 = 0
    c2 = 0
    homonyms_sentences = extract_sentences_from_corpus(gigafida_dirname, homonyms, c1, c2, stop_word_check=True)
    construct_output_temp(homonyms_sentences, corpus_filename, word_limit)
