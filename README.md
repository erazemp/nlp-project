# Project 3: Cross-lingual sense disambiguation
Group name: Absolventi

Group members: Erazem Pušnik, Rok Miklavčič, and Aljaž Šmaljcelj

Advisors: Slavko Žitnik

Organization: University of Ljubljana, Faculty of Computer and Information Science

Course: Natural Language Processing 2021/2022

---

## Description

<p align="center">
 <img src="/data/elmo_bert.jpg" alt="drawing" width="300"/>
</p>
 
The goal of the project is to detect if the context of the same word is different or the same in separate sentences in Slovenian language. 
The Corpus is taken from Gigafida from where we extracted sentences which contain preselected words. 
We intentionally chose words with multiple meanings (ambiguous words).

## Folder structure

Folder `src` contains source code for our project.
It is further divided into subfolders:

* `context_extraction`: contains variable attempts for extracting context from sentences obtained in `preprocess` step. Each attempt will be in its own folder together with source code, final results and evaluation script.
* `preprocess`:
  * `homonyms.py` extracts grouped homonyms from sloWNet and stores them together in a JSON file. Script requires following arguments, editable in `main` function of the script:
    * `homonyms_file`: path to corpus .xml file
    * `output_json`: path to output JSON file, which will be generated, containing all the homonyms
  * `preprocess_sskj.py` transforms gloss words into a list of lemmas that are contained in the gloss. Script requires following arguments, editable in `main` function of the script:
    * `sskj_filename`:  path to SSKJ .xml file
    * `result_filename`: path to output JSON file, containinga list of lemma forms of words in glosses
  * `preprocess_gigafida.py` extracts pairs of sentences with same target word from Gigafida and stores them together in a JSON file. Script returns baseline for further corpus construction to extract context from sentences script requires following arguments, editable in `main` function of the script:
    * `gigafida_dirname`: path to corpus .xml file (that contains only .xml files)
    * `homonyms_filename`: path to file that has homonyms listed line by line in a text file
    * `corpus_filename`: name of the JSON file that is created at the end and contains pairs of sentences which both contain a homonym lemma
    * `word_limit`: limits maximum number of pairs of same lemma sentences a homonym can have
  * `anotate.py` script for assisting with manually annotating corpus
* `validated_corpus` contains manually annotaded data for evaluation purposes

## Instructions (How to run)

In order to run our code, you will first need to install the requirements.
These are stored in `requirements.txt` file in `src` subfolder.
You can install them with the following command

```
cd src
pip install -r requirements.txt
```

### Preprocessing phase

In order to rerun the preprocessing step of extracting information from `ccGigafida` you will to first download, extract and save it in the repository root folder with name `Gigafida_corpus`.
You can download the zip with the following command:

```
curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1035{/ccGigafidaV1_0.zip,/ccGigafida-vert.zip,/ccGigafida-text.zip}
```

If you want to rerun SSKJ preprocess, you can run the main method in `preprocess_sskj.py` file.

If you would like to rerun homonym extraction, you can run the main method in `homonyms.py` file.

### Context extraction phase

Each method we implemented is stored in its own subfolder in `src/context_extraction`.
If you wish to try one of the methods, simply run the main method in the corresponding file (assuming you haven't renamed or moved any files required for running).
Each method creates a new file with `corpus.json` ending which contains labelled data as well as prints the evaluation metrics in standard output.

## Copyright

<footer id="footer">
  <p class="copyright">Absolventi &copy;<a href="<?php bloginfo('url'); ?>" title="<?php bloginfo('name'); ?>home"><?php bloginfo('name'); ?></a> <?php echo date('Y'); ?> All Rights Reserved.</p>
</footer>
