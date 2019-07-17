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
import tqdm

duracionTipo = {'ESCENA': 0, 'PLANO': 0, 'X': 0}

tipos = {
         'HABLADOS' : {'subtipo': {'DIRECTOS':{'duracionTipo': duracionTipo["PLANO"]},
                       'DUBS':{'duracionTipo': duracionTipo["X"]}}},
                       #'S-S-H':{'duracionTipo': duracionTipo["X"]}}, # S-S HABLADO
         'SONIDOS': {'subtipo': {'SONO':{'duracionTipo': duracionTipo["X"]},
                             'S-S':{'duracionTipo': duracionTipo["X"]}}},
         'AMBS': {'duracionTipo': duracionTipo["ESCENA"]},
         'FX': {'duracionTipo': duracionTipo["X"]},
         'MUSICA': {'duracionTipo': duracionTipo["X"]}
         }

sonidista = 'RSM'

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
    c.execute("CREATE TABLE IF NOT EXISTS TRACK(pelicula_id INTEGER, nombre TEXT,tag_id TEXT, id INTEGER PRIMARY KEY, acto TEXT, FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id))")
    c.execute("CREATE TABLE IF NOT EXISTS PELICULA(id INTEGER PRIMARY KEY,nombre TEXT, sonidista TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS AUDIO(id INTEGER PRIMARY KEY, nombre TEXT, duracion INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS REGION(id INTEGER PRIMARY KEY,nombre_audio TEXT, nombre_track TEXT, audio_id INTEGER, track_id INTEGER, into_sample INTEGER, duracion INTEGER, FOREIGN KEY (audio_id) REFERENCES AUDIO (id), FOREIGN KEY (track_id) REFERENCES TRACK (id))")

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
LISTA_PT_TXT_FILES = "/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/DATA/PTF_TXT"

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
                        poblar_audios(linea)

                    if status == 2:
                        pass

                    elif status == 3:
                        #pass
                        poblar_tracks(linea, pelicula_id, acto)

                    elif status == 5:
                        poblar_regiones(linea, pelicula_id)

                    else: pass

            #conn.commit()

                # else:
                #     cambio = False

def poblar_audios(linea):
    char = "`"
    nombre = linea[1: linea[1:-1].find(char) + 1]
    duracion = linea[linea[1:-1].find(char) + 1: -1]
    duracion = linea[linea.find(',') + 1: -1]
    c.execute("INSERT INTO AUDIO (nombre, duracion) VALUES (?, ?)", (nombre, duracion))

def poblar_tracks(linea, pelicula_id, acto):
#TRACK(pelicula_id INTEGER, nombre TEXT,tag_id TEXT, track_id INTEGER, acto TEXT, FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id))")
    char = "`"
    nombre = linea[1: linea[1:-1].find(char) + 1]
    c.execute("INSERT INTO TRACK (pelicula_id,nombre,tag_id, acto) VALUES (?, ?, ?, ?)", (pelicula_id, nombre, None,acto))

def poblar_regiones(linea, pelicula_id):
    #c.execute("DELETE FROM REGION")
#REGION(audio_id INTEGER, track_id INTEGER, into INTEGER, duracion INTEGER)
    char = "`"
    nombre_track = linea[1: linea[1:-1].find(char) + 1]
    char1 = ')'
    char2 = '@'
    #linea = linea[linea[1:-1].find(char2) + 2: -1]
    #print("linea:",linea)
    nombre_audio = linea[linea[1:-1].find(char1) + 4: linea[1:-1].find(char2) - 1]
    #print("track",nombre_track)
    #print("nombre",nombre_audio)
    # c.execute("SELECT id FROM TRACK WHERE pelicula_id = ? AND nombre = ?", (pelicula_id, nombre_track))
    # track_id = c.fetchall()
    # print("TRACK ID:",track_id)
    duracion = linea[linea[1:-1].find(char) + 1: -1]
    duracion = linea[linea.find(',') + 1: -1]
    into_sample = linea[linea.find('@') + 1 : linea.find(',')]

    #TODO AGREGAR ABSOLUTE (TIEMPO EN TRACK)

    #print(into_sample, "into s")
    # c.execute("SELECT id FROM AUDIO WHERE nombre = ? AND duracion = ?", (nombre_audio, duracion))
    # audio_id = c.fetchall()
    # print("AUDIO ID:",audio_id)
    #print(nombre_audio, audio_id, nombre_track, track_id)
    c.execute("INSERT INTO REGION (nombre_audio, nombre_track, into_sample, duracion) VALUES (?, ?, ?, ?)", (nombre_audio, nombre_track, into_sample, duracion))

#leer_Archivo_TXT()
#conn.commit()

# RELACIONAR NOMBRE DE TXT CON NOMBRE ORIGINAL DE ARCHIVO, USANDO .CSV

# LEER TXT
#
# PARA:
#
# ProTools 10 Session: Samplerate = 48000Hz
#
# Target samplerate = 48000
#
# 0 wavs, 0 regions, 0 active regions
#
# PASS


# PARA:
#
# Region (Region#) (WAV#) @ into-sample, length:
#
# MIDI Region (Region#) @ into-sample, length:
#
# PASS


# SI SE ENCUENTRA CON Track name (Track#) (Region#) @ Absolute:

# ABRIR TABLA TRACKS
# INFO EN AUDIOS: TRACK_NRO, TRACK_NOMBRE , TAG, CARDINAL, EXTRA

# SI SE ENCUENTRA CON Track name (Track#) (WAV filename) @ Absolute + Into-sample, Length:

# CREAR RELACIÓN TRACK + AUDIO
# INFO: UBICACIÓN, INICIO + DURACIÓN (ES DECIR, QUÉ FRAGMENTO DEL AUDIO ES USADO EN QUÉ LUGAR DEL TRACK)

