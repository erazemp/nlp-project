import json
import classla


def replace_pronunciation_chars(entry):
    entry = entry.replace('á', 'a')
    entry = entry.replace('à', 'a')
    entry = entry.replace('é', 'e')
    entry = entry.replace('ê', 'e')
    entry = entry.replace('í', 'i')
    entry = entry.replace('ȋ', 'i')
    entry = entry.replace('ó', 'o')
    entry = entry.replace('ô', 'o')
    entry = entry.replace('ú', 'u')
    entry = entry.replace('ŕ', 'r')
    return entry


def make_lemma_sentence(nlp, sentence):
    lemma_sentence = ""
    doc = nlp(sentence)
    for sentence in doc.sentences:
        for token in sentence.tokens:
            lemma_sentence = lemma_sentence + " " + token.words[0].lemma
    return lemma_sentence


def process_sskj(lines):
    nlp = classla.Pipeline('sl', processors='tokenize,ner,pos,lemma')
    entries = {}
    len_lines = str(len(lines))
    for i, line in enumerate(lines):
        if i % 1000 == 0:
            print('processing word', str(i), 'of', len_lines)
        line = replace_pronunciation_chars(line)
        tab_split = line.split('\t')
        if tab_split[0] not in entries:
            entries[tab_split[0]] = []
        explanation = tab_split[1]
        if "1." in explanation and explanation.index("1.") < 30:
            # we have word  with multiple meanings
            i = 1
            while str(i) + "." in explanation:
                split = explanation.split(str(i) + ".")
                i = i + 1
                new_split = split[1].split(str(i) + ".")
                lemma_sentence = make_lemma_sentence(nlp, new_split[0])
                entries[tab_split[0]].append(lemma_sentence)
                i = i + 1
                if len(new_split) > 1:
                    explanation = new_split[1]
                else:
                    break
            expl_lemma_sentence = make_lemma_sentence(nlp, explanation)
            entries[tab_split[0]].append(expl_lemma_sentence)
        else:
            entries[tab_split[0]].append(tab_split[1])
    return entries


def save_to_json_file(filename, entries):
    with open(filename, 'w') as file:
        json.dump(entries, file)


def read_txt_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
    return lines


if __name__ == '__main__':
    sskj_filename = '../../../data/sskj/sskj_definition.txt'
    result_filename = 'preprocessed_sskj.json'
    entries = read_txt_file(sskj_filename)
    processed = process_sskj(entries)
    save_to_json_file(result_filename, processed)
