#Take Review data in csv format
#and process it to
#1. Remove HTML
#2. Remove punctuations
#3. Do Lemmatization
#4. Do stemming
import sqlite3
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('wordnet')
import string
import matplotlib.pyplot as plt
import numpy as np
from nltk.stem import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
import string
import re
import sys
import csv
from nltk.stem.porter import PorterStemmer
stmr= PorterStemmer()
from nltk.corpus import stopwords
import _pickle as cPickle
import csv

regex = re.compile('[%s]' % re.escape(string.punctuation))
def test_re(s):  
    return regex.sub(' ', s)

data=csv.reader(open(sys.argv[1],'r'))
i=0
w=csv.writer(open(sys.argv[2],'w',newline=''))
posSentAll = []
wordsAll = []
for row in data:
		row[-1]=row[-1].rstrip()
		if i==0:
			w.writerow(row)
			i=i+1
			continue


		sents = nltk.sent_tokenize(row[9])
		sents_summary = nltk.sent_tokenize(row[8])
		clean_row1 = ""
		clean_row2 = ""
		for row1 in sents_summary:
			row1 = re.sub("<.*?>", " ", row1)
			row1 = test_re(row1)
			if clean_row1 != "":
				clean_row1 = clean_row1 + " $ " + row1
			else:
				clean_row1 = row1
		for row2 in sents:
			row2 = re.sub("<.*?>", " ", row2)
			row2 = test_re(row2)
			if clean_row2 != "":
				clean_row2 = clean_row2 + " $ " + row2
			else:
				clean_row2 = row2
		clean_row1 = re.sub(r'\d+', ' ', clean_row1)
		clean_row2 = re.sub(r'\d+', ' ', clean_row2)
		words=nltk.word_tokenize(clean_row1)
		clean_row1=''
		for word in words:
			word=word.lower()
			word=lmtzr.lemmatize(word,'n')
			word=lmtzr.lemmatize(word,'v')
			word=lmtzr.lemmatize(word,'a')
			word=lmtzr.lemmatize(word,'r')
			word=stmr.stem(word)
			clean_row1+=' '+word
		words=nltk.word_tokenize(clean_row2)
		clean_row2=''
		for word in words:
			word=word.lower()
			word=lmtzr.lemmatize(word,'n')
			word=lmtzr.lemmatize(word,'v')
			word=lmtzr.lemmatize(word,'a')
			word=lmtzr.lemmatize(word,'r')
			word=stmr.stem(word)
			clean_row2+=' '+word
						
		row[8] = clean_row1.encode('utf-8')
		row[9] = clean_row2.encode('utf-8')
		w.writerow(row)