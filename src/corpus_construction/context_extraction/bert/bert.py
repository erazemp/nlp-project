from scipy.spatial.distance import cosine
from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import nltk
import torch


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
    print(marked_text)
    tokenized_text = tokenizer.tokenize(marked_text)
    print(tokenized_text)
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


if __name__ == '__main__':
    cosine_distance_threshold = 0.7

    # Loading the pre-trained BERT model
    ###################################
    # Embeddings will be derived from
    # the outputs of this model
    # EMBEDDIA/crosloengual-bert
    # bert-base-multilingual-uncased
    model = BertModel.from_pretrained('EMBEDDIA/crosloengual-bert', output_hidden_states=True, )

    # Setting up the tokenizer
    ###################################
    # This is the same tokenizer that
    # was used in the model to generate
    # embeddings to ensure consistency
    tokenizer = BertTokenizer.from_pretrained('EMBEDDIA/crosloengual-bert')

    # Text corpus
    ##############
    # These sentences show the different
    # forms of the word 'bank' to show the
    # value of contextualized embeddings

    texts = ["Ljubljana začeti izhajati ljubljanski časnik slovenski uraden list",
             "izpiten pola pakiran poseben varnosten vrečka izvod skupaj pripadajoč število ocenjevalen obrazec koncepten list",
             "mraz neprijeten vreme hitro zviti svoj cveten list",
             "šopek tulipan oviti zelen list",
             "ugleden evropski list objavljen komentar demokracija kateri beseda",
             "Vida Čadonič Špelič dolenjski list ustanavljanje nov KS Dvor"]

    # Getting embeddings for the target
    # word in all given contexts
    target_word_embeddings = []

    for text in texts:
        tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(text, tokenizer)
        list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model)

        # Find the position 'bank' in list of tokens
        word_index = tokenized_text.index('list')
        # Get the embedding for bank
        word_embedding = list_token_embeddings[word_index]

        target_word_embeddings.append(word_embedding)

    distances_df = calculate_cosine_similarity(texts, target_word_embeddings)
    print(distances_df[distances_df.text1 == 'šopek tulipan oviti zelen list'].to_string())
