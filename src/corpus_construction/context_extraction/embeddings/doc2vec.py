from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import json

from evaluate_doc2vec import perform_evaluation


# UTILS methods
def read_json_file_and_collect_sentences(filename):
    # read JSON file created in preprocess step
    with open(filename, 'r', encoding='utf-8') as file:
        sentences = {}
        data = json.load(file)
        for entry in data:
            target_word = entry["word"]
            if target_word not in sentences:
                sentences[target_word] = []
            sentences[target_word].append(entry["sentence1"])
            sentences[target_word].append(entry["sentence2"])
        return sentences, data


def read_json_files_and_combine_them(filenames, base_path):
    combined = []
    for filename in filenames:
        path = base_path + filename + '_stop_words.json'
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
                else:
                    entry["same_context"] = False
        processed_data.append(entry)
        index = index + 1
    return processed_data


if __name__ == '__main__':
    homonyms = ['klop', 'list', 'postaviti', 'prst', 'surov', 'tema', 'tip']
    json_file = '../../preprocess/preprocessed_data_with_stopwords.json'
    annotated_folder = '../../validated_corpus/'
    results_file = 'doc2vec_corpus.json'
    eval_sentences = read_json_files_and_combine_them(homonyms, annotated_folder)
    sentences, data = read_json_file_and_collect_sentences(json_file)
    eval_sentences.extend(data)
    data = eval_sentences
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
    perform_evaluation(True, annotated_folder, final_result, homonyms)
