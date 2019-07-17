import os
import spacy
import pickle

raiz = '/home/nofi/AUDIOTECA/'


def crear_archivo_lista_de_nombres():

    with open("output2.txt", "w") as a:
        for path, subdirs, files in os.walk(raiz):

            f = subdirs
            a.write(str(f) + os.linesep)

def ext(nombre):
    ext = nombre.split('.', 1)[1:]
    nombre = nombre.split('.', 1)[0]
    return nombre, ext


def tag(nombre):
    nombre, extension = ext(nombre)
    tag = nombre.split(' ', 1)[0]
    nombre = ' '.join(nombre.split()[1:])
    #print ('tag ', tag)
    #print ('resto ', nombre)
    return tag, nombre

def similaridad():
    a = open('output.txt', 'r').read()
    b = open('output2.txt', 'r').read()
    nlp = spacy.load('es')  # make sure to use larger model!
    tokens = nlp(a)
    with open(raiz + 'CLAVES.pck', 'rb') as c:
        CLAVES = pickle.load(c)
        claves = nlp(str(CLAVES))


    for token1 in tokens:

        for token2 in claves:
            if len(token2) == 1:
                pass
            else:
                if  token1.similarity(token2) > 0.9:
                    print(token1.text, token2.text, token1.similarity(token2))

#similaridad()