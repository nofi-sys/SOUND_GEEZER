import six
from google.cloud import translate_v2 as translate
import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/CLAVES/estudionofi-9ce520dea6cb.json"
# Crea una instancia del traductor
translator = translate.Client()

# Lee el archivo JSON
with open('DATA/ontology.json', 'r') as f:
    ontology = json.load(f)

for concept in ontology:

    try:
        concept['name_es'] = translator.translate(concept['name'], target_language='es')["translatedText"]
    except:
        concept['name_es'] = concept['name']
    print(concept['name_es'])
    concept['description_es'] = translator.translate(concept['description'], target_language='es')["translatedText"]
    print(concept['description_es'])

with open('DATA/ontology_es.json', 'w') as f:
    json.dump(ontology, f, ensure_ascii=False)
