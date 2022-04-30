import json


# UTILS methods
def read_json_file(filename):
    # read JSON file created in preprocess step
    with open(filename, "r") as file:
        data = json.load(file)
        return data


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


def count_occurrences(sentence, dict_entry):
    count_list = []
    for entry in dict_entry:
        occurrences = 0
        for word in sentence:
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
    return pairs


if __name__ == '__main__':
    sskj_filepath = '../../preprocess/preprocessed_sskj.json'
    data_filepath = '../../preprocess/preprocessed_data.json'
    results_file = 'simplified_lesk_corpus.json'
    results_part_file = 'simplified_lesk_corpus_part.json'
    sskj_data = read_json_file(sskj_filepath)
    corpus_data = read_json_file(data_filepath)
    updated_pairs = determine_context_pairs(corpus_data, sskj_data)
    save_json_file(updated_pairs, results_file)
    save_part_of_data_for_evaluation(updated_pairs, results_part_file, 50)
