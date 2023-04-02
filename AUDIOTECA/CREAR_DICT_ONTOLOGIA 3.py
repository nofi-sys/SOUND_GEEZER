import pandas as pd
import json

def crear_ontologia_es(elementos):
    # Creamos el data frame
    df = pd.DataFrame(elementos)

    # Creamos el diccionario vacío
    ontologia_es = {}

    # Iteramos sobre los elementos del data frame
    for i, elemento in df.iterrows():
        # Si el elemento es 'abstract', buscamos sus hijos y llamamos de nuevo a la función
        # print(elemento['restrictions'])
        if elemento['restrictions'] == 'abstract':

            # Creamos un diccionario vacío para los hijos
            hijos = {}
            # Iteramos sobre los hijos del elemento
            for id_hijo in elemento['child_ids']:
                # Seleccionamos el hijo del data frame
                try:
                    hijo = df[df['id'] == id_hijo].iloc[0]
                    # print(hijo.values)
                    # Si el hijo tiene restricciones, lo agregamos al diccionario

                    if hijo['restrictions'] == ['abstract']:
                        hijos[hijo['name_es'].values[0]] = crear_ontologia_es(hijo.to_dict('records'))
                    else:
                        # print(hijo['name_es'])
                        hijos[hijo['name_es']] = []
                        # Eliminamos el hijo del data frame
                        df = df[df['id'] != id_hijo]
                except:
                    pass
            # Agregamos el diccionario de hijos al diccionario principal
            ontologia_es[elemento['name_es']] = hijos
        # Si el elemento no es 'abstract', agregamos su nombre al diccionario
        else:
            ontologia_es[elemento['name_es']] = []
            # Eliminamos el elemento del data frame
            df = df[df['id'] != elemento['id']]

    return ontologia_es


# Abre el archivo JSON y carga su contenido en una variable
with open('DATA/ontology_es.json', 'r') as f:
    elementos = json.load(f)
    for elemento in elementos:
        if 'restrictions' in elemento and elemento['restrictions']:
            elemento['restrictions'] = elemento['restrictions'][0]
        else:
            elemento['restrictions'] = ''
# Ahora puedes usar la función crear_ontologia_es con elementos como argumento
ontologia_es = crear_ontologia_es(elementos)
print(ontologia_es)

def organize_dict(d):
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            # Si el valor es un diccionario, llamamos recursivamente a la función
            # con ese diccionario y lo asignamos como valor de la clave actual
            v = organize_dict(v)
            # Si el diccionario no tiene subclaves, lo convertimos en una lista
            if not v.keys():
                v = list(v.keys())
            result[k] = v
        elif k in result:
            # Si la clave ya existe en el diccionario resultado y el valor no es
            # un diccionario, entonces la clave actual debe anidarse bajo la clave
            # existente
            if not isinstance(result[k], dict):
                # Si el valor de la clave existente no es un diccionario, lo convertimos
                result[k] = {None: result[k]}
            # Agregamos la clave actual como subclave del diccionario anidado
            result[k][None] = v
        else:
            # Si la clave no existe, simplemente agregamos el par clave-valor al
            # diccionario resultado
            result[k] = v
    return result
ontologia_es_ok = organize_dict(ontologia_es)
print(ontologia_es_ok)

# Imprime el nombre del primer elemento del diccionario (en este caso, 'Sonidos humanos')
# print(ontologia_es.keys())

# Imprime el nombre del primer subelemento del primer elemento (en este caso, 'Voz humana')
# print(ontologia_es['Sonidos humanos'].keys())

# Imprime la lista de subelementos del primer subelemento del primer elemento (en este caso, ['Habla', 'Gritar', etc.])
# print(ontologia_es['Sonidos humanos']['Voz humana'].keys)

