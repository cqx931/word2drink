
Word2drink is a project that takes textual data from personal life, literature and advertisements, performs emotional analysis based on the word set, and translates the analytical result into a list of ingredients for a glass of drink. By using technologies such as word2vec, natural language processing, it explores flexibility and alternatives in data analysis and creative, absurd interpretation of data by using systematic, logical approaches.

Step 1
Emotion analysis using NRC-Emotion-Lexicon-Wordlevel-v0.92.txt

Step 2
word2vec

----
workflow
python getIngredientVector.py 

python analyzer.py 
python emo2vec.py 
python tsne.py name learning_rate


----

Step 3 
mapping: emotion to drink
`python emoToDrink`

----
Data:
Drink list is based on
http://www.drinksmixer.com/guide/1-1.php
Emotion Lexicon
