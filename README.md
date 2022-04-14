# Project 3: Cross-lingual sense disambiguation
Group name: Dropouts

Group members: Erazem Pušnik, Rok Miklavčič, and Aljaž Šmaljcelj

Advisors: Slavko Žitnik

Organization: University of Ljubljana, Faculty of Computer and Information Science

Course: Natural Language Processing 2020/2021

---

## Description

The goal of the project is to detect if the context of the same word is different or the same in separate sentences in Slovenian language. 
The Corpus will be taken from Gigafida http://eng.slovenscina.eu/korpusi/gigafida or Training Corpus http://eng.slovenscina.eu/tehnologije/ucni-korpus from where we will extract sentences which contain preselected words. We will intentionally chose words with multiple meanings (ambiguous words).

## Folder structure

Folder `src` contains source code for our project.
It is further divided into subfolders:

* `corpus_construction`: contains code for constructing the corpus

  * `preprocess`: contains file `preprocess.py` which extracts pairs of sentences with same target word from Gigafida and stores them together in a JSON file.
  Script returns baseline for further corpus construction to extract context from sentences.
    * script requires following arguments, editable in `main` function of the script:
      * `gigafida_dirname`: path to corpus directory (that contains only .xml files)
      * `homonyms_filename`: path to file that has homonyms listed line by line in a text file
      * `corpus_filename`: name of the JSON file that is created at the end and contains pairs of sentences which both contain a homonym lemma
  * `context_extraction`: contains variable attempts for extracting context from sentences obtained in `preprocess` step. 
  Each attempt will be in its own folder together with source code and final results.

## Instructions (How to run)
 **To-do**

