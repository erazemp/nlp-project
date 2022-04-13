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

## Instructions (How to run)
 **To-do**

