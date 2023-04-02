import spacy
import sqlite3
import re
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm
import spacy
from collections import Counter

# all tokens that arent stop words or punctuations

#%matplotlib inline


conn = sqlite3.connect("/home/nofi/DESARROLLO/ESA/DATA/ptfiles.db")
c = conn.cursor()
nlp = spacy.load('es_core_news_sm')
nlp.max_length = 1500000
#print(nlp.Defaults.stop_words)

c.execute('SELECT * FROM TRACK')

def extraerTag(nombre):
    """RECIBE NOMBRE DE ARCHIVO Y DEVUELVE TAG + NOMBRE  """
   #TODO: FALTA RECONOCER CUANDO LA PRIMERA PALABRA NO ES UN TAG.
   #LA IDEA MÁS INGENUA ES CREAR UNA LISTA DE TAGS
    #print (nombre)
    tag = nombre.split(' ', 1)[0]
    #print (tag)
#    nombre = nombre.split(' ', 1)[1]

   # print('TAG ' + tag)
    #print('NOMBRE ' + nombre)
    return tag

tracks = c.fetchall()
tracks = [track for _, track, _, _, _ in tracks]
#print (tracks)
tags = []
for track in tracks:
    #doc = nlp(track)
    # if track not in tags:
    tags.append(extraerTag(track))
#    print(track)

tags_string = ''
for tag in tags:
    print(tag)
    tags_string = tags_string + tag + " "
    # for token in doc:
    #     extraerTag(token.text)

doc = nlp(tags_string)
print(tags)

words = [token.text for token in doc if token.is_stop != True and token.is_punct != True]

# noun tokens that arent stop words or punctuations
nouns = [token.text for token in doc if token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"]

# five most common tokens
word_freq = Counter(words)
common_words = word_freq.most_common(20)

# five most common noun tokens
noun_freq = Counter(nouns)
common_nouns = noun_freq.most_common(5)

print("PALABRAS ", noun_freq)
print("SUSTANTIVOS ", word_freq)

from spacy import displacy
#
# entities=[(i, i.label_, i.label) for i in doc.ents]
# entities

sns.set(rc= {'figure.figsize': (11.7, 8.27)})
sns.set_style('darkgrid')
