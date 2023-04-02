import pandas as pd
import json
def crear_ontologia(df, elemento, ontologia):
    if elemento['restrictions'] == 'abstract':
        ontologia[elemento['name_es']] = {}
        for id_ in elemento['child_ids']:
            hijo = df[df['id'] == id_].iloc[0]
            crear_ontologia(df, hijo, ontologia[elemento['name_es']])
    else:
        ontologia[elemento['name_es']] = []
        for id_ in elemento['child_ids']:
            hijo = df[df['id'] == id_].iloc[0]
            ontologia[elemento['name_es']].append(hijo['name_es'])

import json

df = pd.read_json('../DATA/ontology_es.json')
# Leemos los datos de 'ontology_es.json'
# with open('DATA/ontology_es.json', 'r') as f:
#     ontologia = json.load(f)

ontologia = {}


for i, elemento in df.iterrows():
    crear_ontologia(df, elemento, ontologia)

print(ontologia)