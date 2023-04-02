
import spacy
import pickle
import os
import pandas as pd

#from TiposGenerales import *

class Clasificar:

    def __init__(self):

        #CARGAR DICCIONARIO CATEGORÍAS
        with open('/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/categorias.pkl', 'rb') as f:
            self.categorias = pickle.load(f)
            # print(self.categorias)

    def UBICAR_EN_AUDIOTECA (self, nombreArchivo):

        #ANALIZAR TIPO (CLASIFICAR POR NOMBRE) PONER ETIQUETA SEGÚN ONTOLOGÍA AUDIOSET (GOOGLE)
        pass

    def CLASIFICAR_POR_NOMBRE(self, nombreArchivo='S-S AULLIDO LEJANO NOCHE.wav'):

        #ANALIZAR NOMBRE DE ARCHIVO PARA ESTIMAR A QUÉ CLASE PERTENECE:

        #RECIBE : NOMBRE
        #ENTREGA:



        #ABREVIATURAS Y EQUIVALENCIAS DE SENTIDO

        # TODO: EXTRAER TAG (TIPO)
        # TIPO: S-S, AMB, DIR, MUSICA, FX. ESTIMAR POR TAG (EJ: SI EL ARCHIVO
        # SE LLAMA "S-S ...") Y SINO, ESTIMAR POR FORMATO DE NOMBRE (EJ: MVI_7048
        # ES UN ARCHIVO DE CÁMARA).

        tag, nombre, extension = self.dividirTagNombreExt(nombreArchivo)

        nlp = spacy.load('es_core_news_lg')
        nombre = nlp(nombre)
        for token in nombre:
            print(token.text, token.pos_, token.dep_, token.rank, token.head.text)

        #extraer la palabra mas importante
        palabra_importante = nombre[0]

        import json

        with open('/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/AUDIOTECA/DATA/ontology_es.json', 'r') as f:
            elementos = json.load(f)
        candidatos = {}
        for elemento in elementos:
            token = nlp(elemento['name_es'].lower())
            if token.similarity(palabra_importante) > 0.75:
                candidatos[token] = token.similarity(palabra_importante)
                # print("el tipo de sonido es: ", elemento['name_es'], " por un porcentaje de ", token.similarity(palabra_importante))  # Imprime el nombre del elemento más similar
        max_value = max(candidatos.items(), key=lambda x: x[1])
        tipo_de_sonido = str(max_value[0])
        print(tipo_de_sonido)

        #EXTRAER RAIZ Y RESTO


    #TODO: HAY QUE ARMAR UN DICT CON ESTA ESTRUCTURA {RAIZ: palabra, RESTO: [RESTO1, ...]}.
            # EN EL FUTURO PODEMOS USAR MAS DATOS DE LAS PALABRAS



        # RESTO: QUITAR STOP WORDS. ENCONTRAR NÚCLEO (EJ: PASOS CEMENTO, "PASOS" ES EL
        # NÚCLEO)

        # INFERIR UBICACIÓN CORRECTA POR UBICACIÓN USUAL DE NÚCLEO. DEBE HABER UNA LISTA
        # DE PALABRAS (NÚCLEOS) COMUNES PARA CADA SECCIÓN DE LA AUDIOTECA.

        # BUSCAR EXCEPCIONES (EJ: SI "PASOS" VA SEGUIDO DE UNA CONSTRUCCIÓN ESPECÍFICA,
        # COMO "PASOS CABALLO") ESTO DEBE ENTENDERSE COMO PASOS DE CABALLO Y POR LO
        # TANTO, IR A ANIMALES.

        #UBICAR SONIDO EN CARPETA CORRECTA

        return tag, nombre,extension

    def CLASIFICAR_POR_AUDIO(self, nombreArchivo, instancia):

        #CHEQUEAR A QUE CLASE PERTENECE ANALIZANDO AUDIO TOMANDO
        #COMO PUNTO DE PARTIDA EL RESULTADO DE LA CLASIFICACIÓN POR NOMBRE

        #LA IDEA ES IMPLEMENTAR ESTO A PARTIR DE MODELO PREEXISTENTE DE TENSOR FLOW

        tipo = 'S-S'
        subtipo = 'SONO'
        return tipo, subtipo

#UTILIDADES
    def dividirTagNombreExt(self, nombreArchivo):

        """RECIBE NOMBRE DE ARCHIVO Y DEVUELVE TAG + NOMBRE  """
        # NORMALIZAR (pasamos a minúscula, borramos puntos y _)
        nombreArchivo, extension = os.path.splitext(nombreArchivo)
        nombreArchivo = nombreArchivo.lower()
        nombreArchivo = nombreArchivo.replace('.', ' ')
        nombreArchivo = nombreArchivo.replace('_', ' ')

        tag, *resto = nombreArchivo.split()
        nombre = " ".join(resto)
        for categoria, etiquetas in self.categorias.items():
            # print(categoria, etiquetas)
            # print("tag ", tag)
            # Si la etiqueta está dentro de la lista de etiquetas de la categoría
            if tag in etiquetas:
                # Asigno a la variable 'tag' la palabra clave (categoría) actual
                tag_ok = categoria
                break
        try:
            tag = tag_ok
        except tag_ok == None:
            tag = '_'


        return tag, nombre, extension


    def ubicarRaiz(self, palabra, resto, path2Audioteca = '/home/nofi/AUDIOTECA/'):

        # RECIBE: UNA FRASE SEPARADA EN RAIZ Y RESTO + EL PATH DE LA AUDIOTECA
        # DEVUELVE: EL PATH FINAL DE UBICACIÓN DEL ARCHIVO


        """El objetivo de esta función es buscar palabras clave en las distintas
        carpetas de la audioteca. Cada carpeta tiene que tener una lista de palabras}
        clave. Si encuentra la palabra en una de esas listas, devuelve el path donde
        se podrá ubicar el archivo"""

        raiz = path2Audioteca

        hits = []
        hitpath = []

        with open(raiz + 'CLAVES.pck', 'rb') as claves:
            CLAVES = pickle.load(claves)

        #ITERAR POR LISTA DE PALABRAS CLAVE, BUSCANDO SI ESTÁ PRESENTE NUESTRA
        # palabra (DADA A LA FUNCIÓN COMO ARGUMENTO).
        for carpeta in CLAVES.keys():
            for subcarpeta in CLAVES[carpeta].keys():

        #DE ENCONTRAR LA PALABRA CLAVE, SUMAR (UBICACIÓN Y PATH) A LISTA DE hits
                #print(CLAVES[carpeta][subcarpeta])
                if palabra in CLAVES[carpeta][subcarpeta].keys():
                    path = path2Audioteca + carpeta + '/' + subcarpeta + '/'
                    hitpath.append(path)
                    hits.append([carpeta, subcarpeta, palabra])
                    print ('HIT: ', CLAVES[carpeta][subcarpeta])
                    print(hits)
                    print(palabra)

        if len(hits) > 1:
            print('AMBIGÜEDAD')
        #SI len(hits) >= 1, tenemos un hit, FIJARSE PUNTAJE DE LA PALABRA CLAVE

        if len(hits) == 1:

        # SI ES < 3   CREAR POPUP PARA OBTENER PERMISO DEL USUARIO. SI ESTÁ OK,
        # DAR UN PUNTO A PALABRA CLAVE PARA ESA UBICACIÓN, COPIAR resto A LISTA EN
        # ESA UBICACIÓN Y return path
            print (hits)
            if CLAVES[hits[0][0]][hits[0][1]][hits[0][2]] < 3:
                #TODO: consultar resultado para evitar falso positivo
                CLAVES[hits[0][0]][hits[0][1]][hits[0][2]] += 1

                #if consultarResultado[0](raiz, hitpath):
                #    CLAVES[hits[0]][hits[1]][hits[2]] += 1
                #    return path
                #else:
                #    return consultarResultado[1]

            else:

                CLAVES[hits[0][0]][hits[0][1]][hits[0][2]] += 1

        else:

            path =  ubicarManualmente(raiz)

        direccion = separar(hitpath[-1])

    #    CLAVES[direccion[-2]][direccion[-1]][palabra] = [1, []]
        print(path)


        return path

    #SI len(hits) > 1 tenemos una ambiguedad.

    #RESOLVER AMBIGUEDAD: COMPARAR RESTO PARA VER SI COINCIDE CON EL RESTO
    #DE CUALQUIER OTRA LISTA. SI COINCIDE EN UNA PALABRA PERO NO EN OTRA, DAR
    #PUNTAJE A ESA PALABRA.


        return path

    def consultarResultado(self, raiz = '/', path = None):

        if path == '/' or no:

            return False, ubicarManualmente(raiz)

        elif si:
            return True, None

        else:
            print ('error')

    def ubicarManualmente(self, raiz = '/', path = None):

        return path

    def separar(self, path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path: # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts



if __name__ == '__main__':
    clasificar = Clasificar()
    print(clasificar.CLASIFICAR_POR_NOMBRE())



    #EJEMPLO DE USO

  #  import TiposGenerales

  #  arch = 'S-S PASOS CEMENTO'

  #  tipo = Tipo (CLASIFICAR_POR_AUDIO(arch, CLASIFICAR_POR_NOMBRE(arch)))


