# getINgredientVector from Spacy pretrained vector model
# Word2drink
# by cqx931 2018.05


#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
import json
from spacy.vectors import Vectors
from spacy.strings import StringStore
nlp = spacy.load('en_core_web_lg')

path = 'drinkList.txt'
output_path = 'drinkVec.json'
def readDataFromFile(loc):
    data = ''
    with open(loc, 'r') as myfile:
        data = myfile.read()
    return data

def loadIngredientFromFile(path):
	il = []
	text = readDataFromFile(path)
	lines = text.split('\n')
	for line in lines:
		if line == "---":
			break
		else:
			il.append(line.lower())
	return il


wordlist = loadIngredientFromFile(path)
tokens = nlp(" ".join(wordlist))

wordVector = dict()

for token in tokens:
	if token.has_vector:
		wordVector[token.text] = list(token.vector.tolist())

with open(output_path, 'w') as fp:
    json.dump(wordVector, fp,sort_keys=True, indent=4)