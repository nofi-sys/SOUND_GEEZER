from googletrans import Translator
#from google_trans_new import google_translator

import json

# Crea una instancia del traductor
translator = Translator()

# Lee el archivo JSON
with open('DATA/ontology.json', 'r') as f:
    ontology = json.load(f)

for concept in ontology:

    try:
        concept['name_es'] = translator.translate(concept['name'], dest='es').text
    except:
        concept['name_es'] = concept['name']
    print(concept['name_es'])
    concept['description_es'] = translator.translate(concept['description'], dest='es').text
    print(concept['description_es'])

with open('DATA/ontology_es.json', 'w') as f:
    json.dump(ontology, f, ensure_ascii=False)
