
import spacy
import es_core_news_sm
import nltk
from NOMBRE_ARCHIVOS_AUDIO import *

nlp = spacy.load('es')
tags = {}

with open('output.txt', 'r') as file:


    for line in file:
        line = line.lower()
        tg, nombre = tag(line)
        #print (tg)
        doc = nlp(tg)

        for token in doc:
            #if token.is_oov:
            try:
                tags[token.text] += 1
            except:
                tags[token.text] = 1
            #print(tags)

            #print('OOV')
            #print(token.text)
            #print(token.shape)
            #for ent in doc.ents:
             #   print (ent)
tags_ok = []
for key in tags.keys():
    if key.isdigit():
        pass
    else:
        if tags[key] > 5:
            print(key, tags[key])
            tags_ok.append(key)

print(tags_ok)

#sorted_d = [(k,v) for k,v in tags.items()]
#print (sorted_d)
#print (tags)