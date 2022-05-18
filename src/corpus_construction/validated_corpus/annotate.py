import json


def annotate(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        file.close()

    for i, entry in enumerate(data):
        word = entry["word"]
        sentence1 = entry["sentence1"]
        sentence2 = entry["sentence2"]
        print(f'sentence1: {sentence1}')
        print(f'sentence2: {sentence2}')
        input_same = input(f'Does the word "{word}" have the same meaning in both sentences? (Y/N, default N)\n')
        if input_same == "Y" or input_same == "y":
            entry["same_context"] = True

        data[i] = entry
        print("\n")

    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    homonyms_file = "./prst.json"
    annotate(homonyms_file)
