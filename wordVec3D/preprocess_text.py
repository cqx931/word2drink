# A pre-process program to clean up the data from txt file
# Word2drink
# by cqx931 2018.05


import sys

# An array to hold the processed script
cleaned_text=[]

file = sys.argv[1]
# Use file system to open the text file 
file1 = open("../text/" + file)
# readlines(), read all lines in a file
lines = file1.readlines()
file1.close()

for line in lines:
	# lines with only white spaces
	if not line.strip():
		continue
	else:
		cleaned_text.append(line)


# `python preprocess_text.py > SampleText_processed.txt`
print("".join(cleaned_text))

