import json
from colorama import Fore, Style


def annotate(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        file.close()

    result = []
    counter = 0
    for i, entry in enumerate(data):
        print(f'counter: {counter}')

        word = entry["word"]
        sentence1 = entry["sentence1"]
        sentence2 = entry["sentence2"]
        start1 = entry["start1"]
        end1 = entry["end1"]
        start2 = entry["start2"]
        end2 = entry["end2"]
        print(f'sentence1: {sentence1[:start1]}{Fore.RED + sentence1[start1:end1] + Style.RESET_ALL}{sentence1[end1:]}')
        print(f'sentence2: {sentence2[:start2]}{Fore.RED + sentence2[start2:end2] + Style.RESET_ALL}{sentence2[end2:]}')
        input_same = input(f'Does the word "{Fore.RED + word + Style.RESET_ALL}" have the same meaning in both sentences? (Y/N/D, default N)\n')
        if input_same == "Y" or input_same == "y":
            entry["same_context"] = True
        elif input_same == "D" or input_same == "d":
            continue

        result.append(entry)
        counter += 1

    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    homonyms_file = "./prst.json"
    annotate(homonyms_file)
