# Emotion to Drink
# Word2drink
# by cqx931 2018.05


#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import spacy
from spacy.vectors import Vectors

# EMOTION_Result_PATH = 'emoVec_3d_50.json'
# Map from Join-Emotion-Vector to Drink-Vector
JOIN_Result_PATH = '../process/facebookAdsText_joinEmoVec_3d_50.json'
Drink_List_PATH = '../process/drinkVec_3d_50.json'

nlp = spacy.load('en_core_web_lg')

#########################
class threedim(object):
    def __init__(self, name, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.name = name

def readJsonToDim(vecs):
	array = []
	for item in vecs:
		x = threedim(item, vecs[item][0],vecs[item][1],vecs[item][2])
		array.append(x)
	return array

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

class VectorDictionary:
	tokens = None

	def __init__(self, path):
		wordlist = loadIngredientFromFile(path)
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
		    print(self.reference[key], key)

def threedimdistance(i, j):
    deltaxsquared = (i.x - j.x) ** 2
    deltaysquared = (i.y - j.y) ** 2
    deltazsquared = (i.z - j.z) ** 2
    return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5
#########################

emoVecs = readJsonToDim(json.loads( open(JOIN_Result_PATH).read()))
drinkVecs = readJsonToDim(json.loads( open(Drink_List_PATH).read()))
result = {}

print(len(emoVecs), len(drinkVecs))
for emo in emoVecs:
	minDistance = 1000
	for drink in drinkVecs:
		dis = threedimdistance(emo, drink)
		if dis < minDistance:
			minDistance = dis
			result[emo.name] = drink.name

for item in result:
	print(item, result[item])




