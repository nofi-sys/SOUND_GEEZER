# ProTools 10 Session: Samplerate = 48000Hz
#
# Target samplerate = 48000
#
# 0 wavs, 0 regions, 0 active regions
#
# Audio file (WAV#) @ offset, length:
#
# Region (Region#) (WAV#) @ into-sample, length:
#
# MIDI Region (Region#) @ into-sample, length:
#
# Track name (Track#) (Region#) @ Absolute:
#
# MIDI Track name (MIDITrack#) (MIDIRegion#) @ Absolute:
#
# Track name (Track#) (WAV filename) @ Absolute + Into-sample, Length:

import sqlite3
import os
import re
#import tqdm

duracionTipo = {'ESCENA': 0, 'PLANO': 0, 'X': 0}

tipos = {
         'HABLADOS' : {'subtipo': {'DIRECTOS':{'duracionTipo': duracionTipo["PLANO"]},
                       'DUBS':{'duracionTipo': duracionTipo["X"]},
                       'OFF':{'duracionTipo': duracionTipo["X"]},
                       'CAM':{'duracionTipo': duracionTipo["X"]}}},
             'SONIDOS': {'subtipo': {'SONO':{'duracionTipo': duracionTipo["X"]},
                             'S-S':{'duracionTipo': duracionTipo["X"]},
                         'PASOS':{'duracionTipo': duracionTipo["X"]}}},
         'AMBS': {'duracionTipo': duracionTipo["ESCENA"]},
         'REF': {'duracionTipo': duracionTipo["X"]},
         'MUSICA': {'duracionTipo': duracionTipo["X"]}
         }

sonidista = 'RSM'

REF = [['REF'], 11]
OFF = [['VOZ', 'OFF', 'VO'], 4]
DUB = [['DUB', 'CASTERMAN',  'MADRE.dup1', 'MADRE', 'LANIÃ\x91A.dup1', 'AGENTE50', 'AGENTE50esc26', 'DOGO', 'LORO', 'LA301bis.dup1', 'MADREBIS.dup1', 'LA301.dup1'], 3]
CAM = [['CAM', 'CAMARA'], 5]
DIR = [['DX', 'DIR','DIR.dup1.06', 'DIR.dup1.01', 'ENTREVISTA', 'DIR.dup1.08', 'H2XY', 'DIR.06', 'DIRECTOS', 'DIR.dup1.07', 'DIR.dup1.03', 'DX2.8', 'DIR.02', 'H2XY.1', 'DIR.dup1.04', 'DIR.05', 'DIR.07', 'DIRBACK', 'H2'], 2]
SN = [['SONO', 'MONOSONO3', 'MONOSONO', 'MONOSONO4', 'MONOSONO5', 'MONOSONO6', 'FX'], 7]
PS = [['PSS','PASOS'], 9]
SS = [['S-S', 'SS', 'ss'], 8]
AMB = [['AMB','AX', 'VIENTOS', 'AMBMONO05', 'AMBMONO06', 'AMB-ST'], 10]
MUS = [['MUSICA', 'MÃ\x9aSICA','MX', 'A12.MUSICA', 'TIMBAL_1', 'CRIOLLA', 'CANCION', 'A11.MUSICA', 'LASS'], 12]

TAG_LIST = [REF, OFF, DUB, CAM, DIR, SN, PS, SS, AMB, MUS]



# ABRIR BASE DE DATOS

def leer_archivo(file):
    data_ptf = []
    with open(file, 'rb') as ptf:
        for line in ptf:
            line = line.decode('ISO-8859-1')
            data_ptf.append(line)
        return data_ptf

conn = sqlite3.connect('ptfiles.db')
c = conn.cursor()

def crear_TABLAS():

    c.execute("CREATE TABLE IF NOT EXISTS TAG(nombre TEXT, id INTEGER PRIMARY KEY, parent_id INTEGER, FOREIGN KEY (parent_id) REFERENCES TAG(id))")
    c.execute("CREATE TABLE IF NOT EXISTS TRACK(pelicula_id INTEGER, nombre TEXT,tag_id INTEGER, id INTEGER PRIMARY KEY, acto TEXT, FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id), FOREIGN KEY (tag_id) REFERENCES TAG (id) ) ")
    c.execute("CREATE TABLE IF NOT EXISTS PELICULA(id INTEGER PRIMARY KEY,nombre TEXT, sonidista TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS AUDIO(id INTEGER PRIMARY KEY, nombre TEXT, duracion INTEGER, pelicula_id INTEGER, FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id) )")
    c.execute("CREATE TABLE IF NOT EXISTS REGION(id INTEGER PRIMARY KEY,nombre_audio TEXT, nombre_track TEXT, audio_id INTEGER, track_id INTEGER, into_track INTEGER,into_sample INTEGER, duracion INTEGER, pelicula_id INTEGER, FOREIGN KEY (audio_id) REFERENCES AUDIO (id), FOREIGN KEY (track_id) REFERENCES TRACK (id), FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id))")

    conn.commit()

crear_TABLAS()

def poblar_Tabla_TAGS():

    indice = 0

    for tipo in tipos:
        c.execute("INSERT INTO TAG (nombre, parent_id) VALUES (?, ?)", (tipo, None))
        indice += 1
        print(tipo, indice)
        parent = indice - 1
        if 'subtipo' in tipos[tipo]:
            print('subtipo')
            for sub in tipos[tipo]['subtipo']:
                print(tipos[tipo]['subtipo'])
                c.execute("INSERT INTO TAG (nombre, parent_id) VALUES (?, ?)", (sub, parent))
                indice += 1
                print(sub)
        parent = indice
    conn.commit()

poblar_Tabla_TAGS()

# LEER LISTA DE TXT, POBLAR TABLA DE PELICULAS
#LISTA_PT_TXT_FILES = "/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/DATA/PTF_TXT"
LISTA_PT_TXT_FILES = "/home/nofi/DESARROLLO/ESA/DATA/PT"

def poblar_Tabla_PELICULAS():


    peliculas = []

    for root, _, files in os.walk(LISTA_PT_TXT_FILES):

        for file in files:
            pelicula = re.split('_', file)
            pelicula = pelicula[0]
            peliculas.append(pelicula)

        print(peliculas)
        peliculas = list(dict.fromkeys(peliculas))
        for peli in peliculas:
            c.execute("INSERT INTO PELICULA (nombre, sonidista) VALUES (?, ?)", (peli, sonidista))
            conn.commit()

poblar_Tabla_PELICULAS()

#IR ABRIENDO UNO POR UNO
def leer_Archivo_TXT():
    nombre_anterior = ''
    for root, _, files in os.walk(LISTA_PT_TXT_FILES):
        for x, file in enumerate(files):
            #ENCONTRAR A QUE PELICULA PERTENECE:
            acto = file
            nombre_pelicula = re.split('_', file)
            nombre_pelicula = nombre_pelicula[0]
            c.execute('SELECT * FROM PELICULA')
            for id, peli, sonidista in c.fetchall():
                if peli == nombre_pelicula:
                    pelicula_id = id

            #print("pelicula id: ", pelicula_id)
            cambio = True
            status = 0

            #EMPEZAR A LEER ARCHIVO TXT
            data_ptf = leer_archivo(root+'/'+file)
            #print(data_ptf[0:9])

            for x, linea in enumerate(data_ptf):
                #print(x)
                if 'Audio file (WAV#) @ offset, length:' in linea:
                #if b'Audio file (WAV#) @ offset, length:\n' in linea:
#                if linea == 'Audio file (WAV#) @ offset, length:':
                    status = 0
                    cambio = True
                    print('AUDIOS')
                elif 'Region (Region#) (WAV#) @ into-sample, length:' in linea:
                    status = 1
                    cambio = True
                    print('REGIONES')
                elif 'MIDI Region (Region#) @ into-sample, length:' in linea:
                    status = 2
                    cambio = True
                    print('REGIONES MIDI')
                elif 'Track name (Track#) (Region#) @ Absolute:' in linea:
                    status = 3
                    cambio = True
                    print("TRACKS")
                elif 'MIDI Track name (MIDITrack#) (MIDIRegion#) @ Absolute:' in linea:
                    status = 4
                    cambio = True
                elif 'Track name (Track#) (WAV filename) @ Absolute + Into-sample, Length:' in linea:
                    track_id_count = 1
                    status = 5
                    cambio = True
                    print("RELACION TRACK-AUDIO")
                else: cambio = False

                # AUDIOS
                # SI SE ENCUENTRA CON 'Audio file (WAV#) @ offset, length:'
                # `MVI_8950.MOV.wav` w(0) @ 0, 710950
                # ABRIR TABLA AUDIOS
                # INFO EN AUDIOS: NOMBRE, DURACIÓN
                # AGREGAR pelicula_id

                if cambio == False:

                    if status == 0:
                        #pass
                        poblar_audios(linea, pelicula_id)

                    if status == 2:
                        pass

                    elif status == 3:
                        #pass
                        nombre_anterior = poblar_tracks(linea, pelicula_id, acto, nombre_anterior)

                    elif status == 5:
                        poblar_regiones(linea, pelicula_id)

                    else: pass

            #conn.commit()

                # else:
                #     cambio = False

def poblar_audios(linea, pelicula_id):
    char = "`"
    nombre = linea[1: linea[1:-1].find(char) + 1]
    duracion = linea[linea[1:-1].find(char) + 1: -1]
    duracion = linea[linea.find(',') + 1: -1]
    c.execute("INSERT INTO AUDIO (nombre, duracion, pelicula_id) VALUES (?, ?, ?)", (nombre, duracion, pelicula_id))

def poblar_tracks(linea, pelicula_id, acto, nombre_anterior):
#TRACK(pelicula_id INTEGER, nombre TEXT,tag_id TEXT, track_id INTEGER, acto TEXT, FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id))")
    char = "`"
    nombre = linea[1: linea[1:-1].find(char) + 1]
    if nombre == nombre_anterior:
        return nombre_anterior
    else:
        tag_id = extraerTag(nombre)
        print(nombre)
        print(tag_id)
        c.execute("INSERT INTO TRACK (pelicula_id,nombre,tag_id, acto) VALUES (?, ?, ?, ?)", (pelicula_id, nombre, tag_id,acto))
        return nombre

def poblar_regiones(linea, pelicula_id):
    #c.execute("DELETE FROM REGION")

# REGION(id INTEGER PRIMARY KEY,nombre_audio TEXT, nombre_track TEXT, audio_id INTEGER, track_id INTEGER, into_track INTEGER,into_sample INTEGER, duracion INTEGER, FOREIGN KEY (audio_id) REFERENCES AUDIO (id), FOREIGN KEY (track_id) REFERENCES TRACK (id))")

    char = "`"
    nombre_track = linea[1: linea[1:-1].find(char) + 1]
    char1 = ')'
    char2 = '@'
    duracion = linea[linea[1:-1].find(char) + 1: -1]
    duracion = linea[linea.find(',') + 1: -1]
    into_sample = linea[linea.find('+') + 1 : linea.find(',')]
    into_track = linea[linea.find('@') + 1 : linea.find('+')]
    nombre_audio = linea[linea[1:-1].find(char1) + 4: linea[1:-1].find(char2) - 1]
    c.execute("INSERT INTO REGION (nombre_audio, nombre_track, into_track, into_sample, duracion, pelicula_id) VALUES (?, ?, ?, ?, ?, ?)", (nombre_audio, nombre_track, into_track, into_sample, duracion, pelicula_id))

def extraerTag(nombre):
    """RECIBE NOMBRE DE ARCHIVO Y DEVUELVE TAG + NOMBRE  """
   #TODO: FALTA RECONOCER CUANDO LA PRIMERA PALABRA NO ES UN TAG.
   #LA IDEA MÁS INGENUA ES CREAR UNA LISTA DE TAGS
    nombre.replace('.', ' ')
    nombre.replace('_', ' ')
    nombre.replace('-', '.')
    tag = nombre.split(' ', 1)[0]
    print("tag ",tag)
    for tipo in TAG_LIST:
        if tag in tipo[0]:
            tag_id = tipo[1]
            return tag_id
    return None


leer_Archivo_TXT()
conn.commit()

# RELACIONAR NOMBRE DE TXT CON NOMBRE ORIGINAL DE ARCHIVO, USANDO .CSV
