# Emotion to Vectors
# Word2drink
# by cqx931 2018.05


#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import spacy
from spacy.vectors import Vectors

fileName = "facebookAdsText"
EMOTION_WORDS_PATH = fileName + 'Words.txt'
EMOTION_RESULT_PATH = fileName + 'Result.json'
output_path1 = fileName + '_emoVec.json'
output_path2 = fileName + '_joinEmoVec.json'
nlp = spacy.load('en_core_web_lg')

emoResult =json.loads( open(EMOTION_RESULT_PATH).read())

def readDataFromFile(loc):
    data = ''
    with open(loc, 'r') as myfile:
        data = myfile.read()
    return data

class VectorDictionary:
	tokens = None

	def __init__(self, wordlist):
		
		tokens = nlp(" ".join(wordlist))
		self.reference = {}
		self.tokens = tokens
		self.vectors = Vectors(shape=(len(wordlist), 300))
		for token in tokens:
			if token.has_vector:
				idx = nlp.vocab.strings[token.text]
				self.reference[idx] = token.text
				self.vectors.add(idx, vector=token.vector)
	def print(self):
		for key in self.vectors.keys():
		    print(self.reference[key], self.vectors[key])


wordlist = readDataFromFile(EMOTION_WORDS_PATH).split(" ")
wordVector = dict()
joinEmoVec = dict()
tokens = nlp(" ".join(wordlist))

for token in tokens:
	if token.has_vector:
		wordVector[token.text] = list(token.vector.tolist())

# calculate joint emoVectors
for emo in emoResult:
	if emo == "positive" or emo == "negative":
		continue
	doc = nlp(" ".join(emoResult[emo]["words"]))
	joinEmoVec[emo] = list(doc.vector.tolist())

print(len(joinEmoVec))
with open(output_path1, 'w') as fp:
    json.dump(wordVector, fp,sort_keys=True, indent=4)
with open(output_path2, 'w') as fp:
    json.dump(joinEmoVec, fp,sort_keys=True, indent=4)
