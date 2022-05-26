from collections import OrderedDict

import numpy as np
from allennlp.commands.elmo import ElmoEmbedder
from sklearn.decomposition import PCA
import json

class Elmo:
    def __init__(self):
        self.elmo = ElmoEmbedder()

    def get_elmo_vector(self, tokens, layer):
        vectors = self.elmo.embed_sentence(tokens)
        X = []
        for vector in vectors[layer]:
            X.append(vector)

        X = np.array(X)

        return X


def dim_reduction(X, n):
    pca = PCA(n_components=n)
    print("size of X: {}".format(X.shape))
    results = pca.fit_transform(X)
    print("size of reduced X: {}".format(results.shape))

    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print("Variance retained ratio of PCA-{}: {}".format(i+1, ratio))

    return results


def calc_values(word, token_list, reduced_X, file_name, title):
    point_values_x = []
    i = 0
    for j, token in enumerate(token_list):
        for _, w in enumerate(token):
            #print("TOKEN: ", token)
            # only plot the word of interest
            # print("WORRDDD", word)
            if w.lower().find(word) != -1 or w.lower().find("postav") != -1 or w.lower().find("tem") != -1:
                #print("stavek: ", sen)
                #print("stavek "+ str(i) + "vrednost: "+ str(reduced_X[i, 0]), str(reduced_X[i, 1]))
                # save point values for euclidian
                point_values_x.append((reduced_X[i, 0], reduced_X[i, 1]))
                                
            i += 1

    tokens = []
    for token in token_list:
        tokens += token

    return point_values_x


def plot(word, token_list, reduced_X, file_name, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    # plot ELMo vectors
    point_values_x = []
    i = 0
    for j, token in enumerate(token_list):
        color = pick_color(j)
        for _, w in enumerate(token):

            # only plot the word of interest
            print("TOKEN: ", token)
           
            if w.lower().find(word) != -1 or w.lower().find("postav") != -1 or w.lower().find("tem") != -1:
                ax.plot(reduced_X[i, 0], reduced_X[i, 1], color)
                #print("stavek: ", sen)
                print("stavek "+ str(i) + "vrednost: "+ str(reduced_X[i, 0]), str(reduced_X[i, 1]))
                # save point values for euclidian
                point_values_x.append((reduced_X[i, 0], reduced_X[i, 1]))
                                
            i += 1

    tokens = []
    for token in token_list:
        tokens += token
    
    

    # annotate point
    k = 0
    for i, token in enumerate(tokens):
        if token.lower() in [word, 'postav' 'prstjo', 'prstom', 'prsti', 'prstov', 'prst', word + 's', word + 'ing', word + 'ed']:
            text = ' '.join(token_list[k])

            # bold the word of interest in the sentence
            text = text.replace(token, r"$\bf{" + token + "}$")

            plt.annotate(text, xy=(reduced_X[i, 0], reduced_X[i, 1]))
            k += 1

    ax.set_title(title)
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    fig.savefig(file_name, bbox_inches="tight")

    print("{} saved\n".format(file_name))
    
    return point_values_x


def pick_color(i):
    if i == 0:
        color = 'ro'
    elif i == 1:
        color = 'bo'
    elif i == 2:
        color = 'yo'
    elif i == 3:
        color = 'go'
    else:
        color = 'co'
    return color


def calc_distance(points_tab):
    a = np.array(points_tab[0])
    b = np.array(points_tab[1])
    dist = np.linalg.norm(a - b)
    return dist

def read_json_files_and_combine_them(filenames, base_path):
    combined = []
    for filename in filenames:
        path = base_path + filename + '_stop_words' + '.json'
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            combined.extend(data)
    return combined

def fill_corpus(corpus_ent, th, dist):
    if th <= dist:
        corpus_ent["same_context"] = False
    else:
        corp_ent["same_context"] = True
    return corpus_ent

def save_json_file(pairs, json_filename):
    print('Saving to JSON file')
    json_str = json.dumps([p for p in pairs], indent=2, ensure_ascii=False)
    # save to JSON file
    with open(json_filename, "w", encoding='utf-8') as outfile:
        outfile.write(json_str)



if __name__ == "__main__":
    model = Elmo()

    prst = OrderedDict()
    prst[0] = "Med tiste, ki bodo pravilno odgovorili na postavljeno vprašanje( eno smo postavili pretekli teden), bomo z žrebom razdelili deset vstopnic za koncert R."
    prst[1] = "Multiuspešne ženske skupine, kot so All Saints, TLC in Destiny's Child, so tiste, ki pravzaprav nosijo hlače, ki se znajo veliko bolje postaviti za svoje interese."
    prst[2] = "Tunizijski veščak na arabski lutnji, al ud, se je na prejšnjem albumu postavil z jazzovskim triom, z Davom Hollandom in Johnom Surmanom."
    prst[3] = "Mediji so se v katoliški Italiji presenetljivo postavili na stran zaljubljencev, poroka pa je bila vseeno v Švici."
    prst[4] = "Postavili smo torej mejo 85.000 tolarjev( z vštetim DDV) in na trgu našli kar sedem monitorjev, ki cenovno sodijo v to omejitev."
    prst[5] = "Poleg obeh naprav v paketu dobimo tudi majhen plastični podstavek, ki omogoča, da bralnik postavimo na bok, ko ga ne potrebujemo."
    prst[6] = "Kraj, ki ga ni na karti, je pravzaprav samo mestece, nič kaj večje od kakih dvestotih ducatov avtodomov, če jih postaviš enega ob drugega."
    prst[7] = "Preden namreč spelje tak tovornjak, ki se je postavil v sredino križišča, da bi zavil levo, se spet prižge rdeča luč."
              

    works = OrderedDict()
    works[0] = "I like this beautiful work by Andy Warhol"
    works[1] = "Employee works hard every day"
    works[2] = "My sister works at Starbucks"
    works[3] = "This amazing work was done in the early nineteenth century"
    works[4] = "Hundreds of people work in this building"

    plants = OrderedDict()
    plants[0] = "The gardener planted some trees in my yard"
    plants[1] = "I plan to plant a Joshua tree tomorrow"
    plants[2] = "My sister planted a seed and hopes it will grow to a tree"
    plants[3] = "This kind of plant only grows in the subtropical region"
    plants[4] = "Most of the plants will die without water"



    homonyms = ['postaviti', 'surov', 'tema', 'tip', 'klop', 'list', 'prst']
    validated_corpus_location = 'corpus/'
    result_file = 'corpus/elmo_corpus.json'

    corpus_entries = read_json_files_and_combine_them(homonyms, validated_corpus_location)
    print(corpus_entries)

    # contextual vectors for ELMo layer 1 and 2 
    
    k = 0
    threshold = 1.7
    corp_dict = []
    for i, entry in enumerate(corpus_entries):
        print("000000000000000000000")
        word = OrderedDict()
        word[0] = entry["sentence1"]
        word[1] = entry["sentence2"]
                
        words = {
            entry["word"]: word,
        }

        for layer in [1]:
            sentence_values_x = []
            for word, sentences in words.items():
                print("visualizing word {} using ELMo layer {}".format(word, layer))
                X = np.concatenate([model.get_elmo_vector(tokens=sentences[idx].split(),
                                                          layer=layer)
                                    for idx, _ in enumerate(sentences)], axis=0)

                
                # The first 2 principal components
                X_reduce = dim_reduction(X=X, n=2)

                token_list = []
                for _, sentence in sentences.items():
                    token_list.append(sentence.split())

                file_name = "{}_elmo_layer_{}.png".format(word, layer)
                title = "Layer {} ELMo vectors of the word {}".format(layer, word)
                val_x = calc_values(word, token_list, X_reduce, file_name, title)
                #val_x = plot(word, token_list, X_reduce, file_name, title)
                for tup in val_x:
                  sentence_values_x.append(tup)          
                print("TOCKE VREDNOSTI: ", sentence_values_x)
                e_dist = calc_distance(sentence_values_x)
                corp_ent = fill_corpus(entry, threshold, e_dist)
                corp_dict.append(corp_ent)
    print(corp_dict)
    save_json_file(corp_dict, result_file)











































