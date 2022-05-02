from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import json


# UTILS methods
def read_json_file_and_collect_sentences(filename):
    # read JSON file created in preprocess step
    with open(filename, "r") as file:
        sentences = {}
        data = json.load(file)
        for entry in data:
            target_word = entry["word"]
            if target_word not in sentences:
                sentences[target_word] = []
            sentences[target_word].append(entry["sentence1"])
            sentences[target_word].append(entry["sentence2"])
        return sentences, data


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


def generate_context(data, model, target_word, length):
    processed_data = []
    index = 0
    for entry in data:
        if entry["word"] != target_word:
            continue
        sentence2_index = index * 2 + 1
        tokenized1 = word_tokenize(entry["sentence1"].lower())
        vector1 = model.infer_vector(tokenized1)
        similar = model.docvecs.most_similar(positive=[vector1], topn=length)
        for sim in similar:
            if sim[0] == sentence2_index:
                score = sim[1]
                if score > 0.45:
                    entry["same_context"] = True
        processed_data.append(entry)
        index = index + 1
    return processed_data


if __name__ == '__main__':
    json_file = '../../preprocess/preprocessed_data.json'
    results_file = 'doc2vec_corpus.json'
    results_part_file = 'doc2vec_corpus_part.json'
    sentences, data = read_json_file_and_collect_sentences(json_file)
    # Tokenization of each document
    final_result = []
    for word in sentences:
        print('processing word', word)
        se = sentences[word]
        tokenized_sent = []
        for s in se:
            tokenized_sent.append(word_tokenize(s.lower()))
        tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]
        model = Doc2Vec(tagged_data, vector_size=100, window=2, min_count=1, epochs=100)
        result = generate_context(data, model, word, len(se))
        final_result.extend(result)
    save_json_file(final_result, results_file)
    save_part_of_data_for_evaluation(final_result, results_part_file, 50)
