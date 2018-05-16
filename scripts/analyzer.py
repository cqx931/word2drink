# Emotion Analyzer from Facebook messages
# Word2drink
# by cqx931 2018.05


#!/usr/bin/python
# -*- coding: utf-8 -*-
import spacy
import re
import json
from preshed.counter import PreshCounter

# spacy's default English language model doesn't have word
# vector data, so we must use a larger variant to use vectors.
# Here's how to download a large model for English:
#  python -m spacy download en_core_web_lg

nlp = spacy.load('en_core_web_lg')
fileName = "facebookAdsText"
# emotion data
dbug = False
EMOTION_DATA_PATH = '../data/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
TEXT_PATH  = '../data/'+ fileName +'.txt'

#############

def countTheWords(doc):
    counts = PreshCounter()

    for word in doc:
        counts.inc(word.orth, 1)
    for (word_id, count) in counts:
        print (count, nlp.vocab.strings[word_id])
    return counts


def readDataFromFile(loc):
    data = ''
    with open(loc, 'r') as myfile:
        data = myfile.read()
    return data

def parseTextFromHtml(html):
    text = ""
    try: 
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    allResult = soup.find_all("div", class_="_3-96 _2let")
    for item in allResult:
        text += item.text + "\n"
    return text

def processData(data):
    if 'html' in TEXT_PATH:
        text = parseTextFromHtml(data)
    else:
        text = data
    return text

def getEmotionFromIdx(i):
    emotions = [
        'anger',
        'anticipation',
        'disgust',
        'fear',
        'joy',
        'negative',
        'positive',
        'sadness',
        'surprise',
        'trust',
        ]
    return emotions[i]

# pretty print dictionary
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

class EmotionEntry:

    text = ''
    emotions = {}
    
    def __init__(self, text):
        self.text = text
        self.emotions = {
            "anger": 0,
            "anticipation": 0,
            "disgust": 0,
            "fear": 0,
            "joy": 0,
            "negative": 0,
            "positive": 0,
            "sadness": 0,
            "surprise": 0,
            "trust": 0
            }
    def set(self,emo, value):
        self.emotions[emo] = value

class EmotionDict:

    size = 0
    entries = {}

    def __init__(self, path):
        text = readDataFromFile(path)
        lines = text.split('\n')
        size = int(len(lines) / 10)
        entries = {}
        for i in range(size):
            word = re.match(r'([^\t]+)',lines[i * 10]).group(0)
            entry = EmotionEntry(word)
            for j in range(10):
                line = lines[i * 10 + j]
                if '1' in line:
                    emotion = getEmotionFromIdx(j)
                    entry.set(emotion, 1)
                    entries[entry.text] = entry.emotions
        self.size = len(entries)
        self.entries = entries
    def __str__(self):
         pretty(self.entries)
         return "Total Entries: " + str(self.size)
    def saveToTxt(self, fileName):
         emoList = self.entries.keys()
         string = " ".join(emoList)
         text_file = open("fileName", "w")
         text_file.write(string)
         text_file.close()
         return 

class EmotionCounter():
    wordCount = 0
    doc = None
    validWords = []

    def __init__(self, text):
        self.text = text
        self.doc = None
        self.emoWords = "" #all the emotionlly charged words
        self.wordCount = 0
        self.validWords = []
        self.emotions = {
            "anger": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "anticipation": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "disgust": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "fear": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "joy": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "negative": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "positive": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "sadness": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "surprise": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            },
            "trust": {
              "score": 0,
              "percentage": 0,
              "words":[],
              "count": {}
            }
            }

    def analyze(self, emoDict):
        doc = self.doc = nlp.tokenizer(text)
        for token in doc:
            if dbug and token.is_oov:
                print("!Token out of vocab:", token)
                print('Vector for %s:' % token, token.vector)
            if token.is_alpha:
                word = token.lemma_.lower()
                self.wordCount += 1
                if word in emoDict.entries:
                    self.validWords.append(word)
                    entry = emoDict.entries[word]
                    for emotion in self.emotions:
                        if entry[emotion] == 1:
                            self.emotions[emotion]["score"] += 1
                            self.emotions[emotion]["words"].append(word)
                            if word not in self.emoWords: self.emoWords += word + " "
                            if word in self.emotions[emotion]["count"]: # count 
                              self.emotions[emotion]["count"][word] +=1
                            else: # add the word if doesn't exist
                              self.emotions[emotion]["count"][word] = 1

        self.calculatePercentage()
    
    def calculatePercentage(self):
        for emo in self.emotions:
            this =  self.emotions[emo]
            this["percentage"] = this["score"] / self.wordCount

    def getValidWords(self, range=None):
        if range == None:
            return self.validWords
        else:
            return self.emotions[range]["words"]
    
    def floatToPercentage(self, f):
        return str("{0:.2f}".format(f*100)) + "%"

    def printScores(self):
        for emo in self.emotions:
            print(emo, self.emotions[emo]["score"], self.floatToPercentage(self.emotions[emo]["percentage"]))
    
    def __str__(self):
        pretty(self.emotions)
        return "Text length is: " + str(len(self.doc)) + "\n" + "Word Count is:" + str(self.wordCount)

######################
data = readDataFromFile(TEXT_PATH)
text = processData(data)

emoDict = EmotionDict(EMOTION_DATA_PATH)
emoDict.saveToTxt("list.txt")
# print(text)
emoResult = EmotionCounter(text)
emoResult.analyze(emoDict)
# print(emoResult.wordCount)
# emoResult.printScores()
print(emoResult.emoWords)
with open(fileName + 'Words.txt', 'w') as outfile:
    json.dump(emoResult.emoWords, outfile)
with open(fileName + 'Result.json', 'w') as outfile:
    json.dump(emoResult.emotions, outfile)
