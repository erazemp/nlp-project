import pandas as pd
import torch
import json
from scipy.spatial.distance import cosine
from transformers import BertTokenizer, BertModel
from evaluate import perform_evaluation


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


def construct_bert(model_path, pairs):
    # Loading the pre-trained BERT model
    ###################################
    # Embeddings will be derived from
    # the outputs of this model
    # EMBEDDIA/crosloengual-bert
    # bert-base-multilingual-uncased
    model = BertModel.from_pretrained(model_path, output_hidden_states=True, )

    # Setting up the tokenizer
    ###################################
    # This is the same tokenizer that
    # was used in the model to generate
    # embeddings to ensure consistency
    tokenizer = BertTokenizer.from_pretrained(model_path)

    cos_distances = []

    for pair in pairs:
        word = pair["word"]
        sentence1 = pair["lemma_sentence1"]
        sentence2 = pair["lemma_sentence2"]
        texts = [sentence1, sentence2]

        # Getting embeddings for the target
        # word in all given contexts
        target_word_embeddings = []

        for text in texts:
            tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(text, tokenizer)
            list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model)

            # Find the position of the word in list of tokens
            word_index = tokenized_text.index(word)
            # Get the embedding for bank
            word_embedding = list_token_embeddings[word_index]

            target_word_embeddings.append(word_embedding)

        distances_df = calculate_cosine_similarity(texts, target_word_embeddings)
        # print(distances_df[distances_df.text1 == sentence1].to_string())
        print(distances_df[distances_df.text1 == sentence1].to_numpy()[1][2])
        cos_distances.append(distances_df[distances_df.text1 == sentence1].to_numpy()[1][2])

    return cos_distances


def bert_text_preparation(text, tokenizer):
    """Preparing the input for BERT

    Takes a string argument and performs
    pre-processing like adding special tokens,
    tokenization, tokens to ids, and tokens to
    segment ids. All tokens are mapped to seg-
    ment id = 1.

    Args:
        text (str): Text to be converted
        tokenizer (obj): Tokenizer object
            to convert text into BERT-re-
            adable tokens and ids

    Returns:
        list: List of BERT-readable tokens
        obj: Torch tensor with token ids
        obj: Torch tensor segment ids


    """
    marked_text = "[CLS] " + text + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = [1] * len(indexed_tokens)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    return tokenized_text, tokens_tensor, segments_tensors


def get_bert_embeddings(tokens_tensor, segments_tensors, model):
    """Get embeddings from an embedding model

    Args:
        tokens_tensor (obj): Torch tensor size [n_tokens]
            with token ids for each token in text
        segments_tensors (obj): Torch tensor size [n_tokens]
            with segment ids for each token in text
        model (obj): Embedding model to generate embeddings
            from token and segment ids

    Returns:
        list: List of list of floats of size
            [n_tokens, n_embedding_dimensions]
            containing embeddings for each token

    """

    # Gradient calculation id disabled
    # Model is in inference mode
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        # Removing the first hidden state
        # The first state is the input state
        hidden_states = outputs[2][1:]

    # Getting embeddings from the final BERT layer
    token_embeddings = hidden_states[-1]
    # Collapsing the tensor into 1-dimension
    token_embeddings = torch.squeeze(token_embeddings, dim=0)
    # Converting torchtensors to lists
    list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]

    return list_token_embeddings


def calculate_cosine_similarity(texts, target_word_embeddings):
    # Calculating the distance between the
    # embeddings of 'bank' in all the
    # given contexts of the word

    list_of_distances = []
    for text1, embed1 in zip(texts, target_word_embeddings):
        for text2, embed2 in zip(texts, target_word_embeddings):
            cos_dist = 1 - cosine(embed1, embed2)
            list_of_distances.append([text1, text2, cos_dist])

    distances_df = pd.DataFrame(list_of_distances, columns=['text1', 'text2', 'distance'])

    return distances_df


def fill_corpus(corpus_entries, cos_distances, cosine_distance_threshold):
    for i, entry in enumerate(corpus_entries):
        if cos_distances[i] > cosine_distance_threshold:
            entry["same_context"] = True

        corpus_entries[i] = entry
    return corpus_entries


if __name__ == '__main__':
    # homonyms = ['klop', 'list', 'postaviti', 'prst', 'surov', 'tema', 'tip']
    homonyms = ['list']
    validated_corpus_location = '../../validated_corpus/'
    results_file = 'bert_corpus.json'
    part_results_file = 'bert_corpus_part.json'
    cosine_distance_threshold = 0.7
    model_path = 'EMBEDDIA/crosloengual-bert'
    # model_path = 'bert-base-multilingual-uncased'

    corpus_entries = read_json_files_and_combine_them(homonyms, validated_corpus_location)
    cos_distances = construct_bert(model_path, corpus_entries)
    corpus_entries = fill_corpus(corpus_entries, cos_distances, cosine_distance_threshold)
    save_json_file(corpus_entries, results_file)
    perform_evaluation(False, validated_corpus_location, corpus_entries, homonyms)
