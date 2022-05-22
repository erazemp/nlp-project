import json


def perform_evaluation(include_stopwords, path_to_validated_corpus, results, homonyms):
    total_tn = 0
    total_fn = 0
    total_fp = 0
    total_tp = 0
    for homonym in homonyms:
        tn = 0
        fn = 0
        fp = 0
        tp = 0
        # retrieve annotated data from homonyms
        filename = path_to_validated_corpus
        if include_stopwords:
            filename += homonym + '_stop_words.json'
        else:
            filename += homonym + '.json'
        with open(filename, 'r', encoding='utf-8') as file:
            annotated_data = json.load(file)
            # find corresponding sentence that is annotated
            for annotated in annotated_data:
                predicted = find_matching_record(annotated, results)
                annotated_context = annotated["same_context"]
                prediction_context = predicted["same_context"]
                if annotated_context:
                    if prediction_context:
                        tp = tp + 1
                    else:
                        fn = fn + 1
                else:
                    if prediction_context:
                        fp = fp + 1
                    else:
                        tn = tn + 1
        print('Evaluation for word', homonym)
        print('TP:', tp, 'TN', tn, 'FP:', fp, 'FN:', fn)
        print('----------------------------------------')
        total_fp = total_fp + fp
        total_fn = total_fn + fn
        total_tn = total_tn + tn
        total_tp = total_tp + tp
    print('Total evaluation:')
    print('TP:', total_tp, 'TN', total_tn, 'FP:', total_fp, 'FN:', total_fn)
    print('----------------------------------------')
    print('Total recall, precision, F1 Score, Accuracy')
    print(total_tp / (total_tp + total_fn), total_tp / (total_tp + total_fp), 2 * total_tp / (2 * total_tp + total_fp + total_fn),
          (total_tp + total_tn) / (total_tp + total_tn + total_fp + total_fn))


def find_matching_record(result, predicted):
    for data in predicted:
        if result["sentence1"] == data["sentence1"] and result["sentence2"] == data["sentence2"]:
            return data
