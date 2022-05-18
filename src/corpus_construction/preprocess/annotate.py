import json
from colorama import Fore, Style


def annotate(filename, filename_stop_words):
    with open(filename_stop_words, 'r', encoding='utf-8') as file:
        data_stop_words = json.load(file)
        file.close()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        file.close()

    result_stop_words = []
    result = []
    counter = 0
    for i, entry in enumerate(data_stop_words):
        print(f'counter: {counter}')

        word = entry["word"]
        sentence1 = entry["sentence1"]
        sentence2 = entry["sentence2"]
        start1 = entry["start1"]
        end1 = entry["end1"]
        start2 = entry["start2"]
        end2 = entry["end2"]
        print(f'sentence1: {sentence1[:start1]}{Fore.RED + sentence1[start1:end1 + 1] + Style.RESET_ALL}{sentence1[end1 + 1:]}')
        print(f'sentence2: {sentence2[:start2]}{Fore.RED + sentence2[start2:end2 + 1] + Style.RESET_ALL}{sentence2[end2 + 1:]}')
        input_same = input(f'Does the word "{Fore.RED + word + Style.RESET_ALL}" have the same meaning in both sentences? (Y/N/D, default N)\n')
        if input_same == "Y" or input_same == "y":
            entry["same_context"] = True
        elif input_same == "D" or input_same == "d":
            continue

        result_stop_words.append(entry)
        counter += 1

        data[i]["same_context"] = entry["same_context"]
        result.append(data[i])

    with open(filename_stop_words, "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(result_stop_words, indent=2, ensure_ascii=False))

    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    corpus_file = "../validated_corpus/tema.json"
    corpus_file_stop_words = "../validated_corpus/tema_stop_words.json"
    annotate(corpus_file, corpus_file_stop_words)
