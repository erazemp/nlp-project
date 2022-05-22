import json

from evaluate_lesk import perform_evaluation

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


def count_occurrences(sentence, dict_entry):
    count_list = []
    for entry in dict_entry:
        occurrences = 0
        sentence_split = sentence.split()
        for word in sentence_split:
            if word in entry:
                occurrences = occurrences + 1
        count_list.append(occurrences)
    max_value = max(count_list)
    return count_list.index(max_value)


def determine_context_pairs(pairs, sskj):
    for pair in pairs:
        target_word = pair["word"]
        if target_word in sskj:
            sskj_entry = sskj[target_word]
            if len(sskj_entry) == 0 or len(sskj_entry) == 1:
                pair["same_context"] = True
            else:
                sentence1 = pair["lemma_sentence1"]
                s1_context = count_occurrences(sentence1, sskj_entry)
                sentence2 = pair["lemma_sentence2"]
                s2_context = count_occurrences(sentence2, sskj_entry)
                if s1_context == s2_context:
                    pair["same_context"] = True
                else:
                    pair["same_context"] = False
    return pairs


if __name__ == '__main__':
    homonyms = ['klop', 'list', 'postaviti', 'prst', 'surov', 'tema', 'tip']
    validated_corpus_location = '../../validated_corpus/'
    sskj_filepath = '../../preprocess/preprocessed_sskj.json'
    data_filepath = '../../preprocess/preprocessed_data.json'
    results_file = 'simplified_lesk_corpus.json'
    sskj_data = read_json_file(sskj_filepath)
    # construct and save main (Gigafida) corpus
    corpus_data = read_json_file(data_filepath)
    updated_pairs = determine_context_pairs(corpus_data, sskj_data)
    save_json_file(updated_pairs, results_file)
    # construct and evaluate from test corpus
    print('Starting evaluation step')
    corpus_data_eval = read_json_files_and_combine_them(homonyms, validated_corpus_location)
    updated_pairs_eval = determine_context_pairs(corpus_data_eval, sskj_data)
    perform_evaluation(False, validated_corpus_location, updated_pairs_eval, homonyms)
