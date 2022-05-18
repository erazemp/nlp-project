import json

if __name__ == '__main__':
    filename = "../validated_corpus/list.json"
    filename_stop_words = "../validated_corpus/list_stop_words.json"

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        file.close()

    with open(filename_stop_words, 'r', encoding='utf-8') as file:
        data_stop_words = json.load(file)
        file.close()

    for i, entry in enumerate(data):
        entry["same_context"] = data_stop_words[i]["same_context"]
        data[i] = entry

    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(data, indent=2, ensure_ascii=False))
