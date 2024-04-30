import os
import re
import codecs
import matplotlib.pyplot as plt
import collections
from string import punctuation
import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.corpus import webtext
from nltk.corpus import gutenberg
import spacy

words_r = reuters.words()
words_b = brown.words()
words_w = webtext.words()
words_g = gutenberg.words()

brown_words = dict(collections.Counter([lemmatizer.lemmatize(i.lower()) for i in words_b]))
reuters_words = dict(collections.Counter([lemmatizer.lemmatize(i.lower()) for i in words_r]))
web_words = dict(collections.Counter([lemmatizer.lemmatize(i.lower()) for i in words_w]))
guten_words = dict(collections.Counter([lemmatizer.lemmatize(i.lower()) for i in words_g]))

nlp = spacy.load("en_core_web_sm")
stop = set(stopwords.words('english'))


stop_brown = [i[0] for i in sorted(brown_words.items(), key=lambda k: k[1], reverse=True) if i[1] > 100]
stop_reuters = [i[0] for i in sorted(reuters_words.items(), key=lambda k: k[1], reverse=True) if i[1] > 250]
stop_web = [i[0] for i in sorted(web_words.items(), key=lambda k: k[1], reverse=True) if i[1] > 50]
stop_guten = [i[0] for i in sorted(guten_words.items(), key=lambda k: k[1], reverse=True) if i[1] > 100]

BASE_DIR = 'data'
DATA_DIR = codecs.open(os.path.join(BASE_DIR, 'books/HP1.txt'), 'rb', encoding='utf-8').readlines()
COMMON_DIR = codecs.open(os.path.join(BASE_DIR, 'google_10000.txt'), 'rb', encoding='utf-8').readlines()
true_data = pd.read_csv(os.path.join(BASE_DIR, 'ground_truth/HP1.csv'), sep='\t')
stop_words = codecs.open(os.path.join(BASE_DIR, 'stop.txt'), 'rb', encoding='utf-8').readlines()
