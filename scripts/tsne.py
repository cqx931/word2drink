# Using tsne to reduce the data to 3D
# Using sklearn t-sne
# Word2drink
# by cqx931 2018.05


# python 2
import json
import sys
import numpy as np
from sklearn.manifold import TSNE

file_name  = sys.argv[1]
lr = int(sys.argv[2])
# source_path = '../word_vector_pretrained_data/' + file_name +"/" + file_name +"_gensim_result.json"
# output_path = '../word_vector_pretrained_data/' + file_name +"/" + file_name + "_2d_vector_result_200.json"
source_path = file_name + '.json'
output_path = file_name + '_3d_' + str(lr) +'.json'

# Load raw json data
raw_vectors =json.loads( open(source_path).read())

# Create two list to store words and their vectors separately
vector_list = list()
word_list = list()
for value in raw_vectors.values():
    vector_list.append(value)
for key in raw_vectors.keys():
    word_list.append(key)


sizedown_vector = list()

# TSNE
# Create a numpy array from vector list()
X = np.asarray(vector_list).astype('float64')
# Convert it to a 3 dimensional vector space
# Parameters matters

# The learning rate for t-SNE is usually in the range [10.0, 1000.0]. 
# If the learning rate is too high, the data may look like a ‘ball’ 
# with any point approximately equidistant from its nearest neighbours. 
# If the learning rate is too low, most points may look compressed in a dense cloud with few outliers.
tsne_model = TSNE(n_components=3, early_exaggeration=8.0, learning_rate=lr, random_state=0)
np.set_printoptions(suppress=True)
#.fit_transform: fit X into an embeded space and return that transformed output
#.tolist(): use tolist() to convert numpy array into python list data structure 
sizedown_vector = tsne_model.fit_transform(X).tolist()

# create a result dictionary to hold the combination of word and its new vector
result_vectors = dict()
for i in range(len(word_list)):
    result_vectors[word_list[i]] = sizedown_vector[i]


with open(output_path, 'w') as fp:
    json.dump(result_vectors, fp,sort_keys=True, indent=4)
