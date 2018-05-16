# Using tsne to reduce the data to 3D
# Using sklearn t-sne
# Word2drink
# by cqx931 2018.05


# python 3
import json
import sys
import numpy as np
from sklearn.manifold import TSNE

file_name  = sys.argv[1]
mode = sys.argv[2] #emotion or drink

source_path = '../word_vector_pretrained_data/' + file_name +"/" + file_name + "_3d_vector_result_200.json"
emo_path = '../scripts/emoList.txt'
drink_path = '../scripts/drinkList.txt'
output_path = '../word_vector_pretrained_data/' + file_name +"/" + file_name + "_200_filtered_" + mode +".json"

def filter(raw, filter):
	l = dict()
	for entry in raw:
		if entry in filter:
			l[entry] = raw[entry]
	print("Filtered:" + str(len(l)))
	return l


myFilter = []
raw_vectors = json.loads( open(source_path).read())

if mode == "drink":
	myFilter = open(drink_path).read().lower().split("\n")
else:
	myFilter = open(emo_path).read().split(" ")

print(len(myFilter))
filtered = filter(raw_vectors , myFilter)

with open(output_path, 'w') as fp:
    json.dump(filtered, fp,sort_keys=True, indent=4)
