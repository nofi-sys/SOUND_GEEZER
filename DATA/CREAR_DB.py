import os
from datetime import datetime
import sqlite3

conn = sqlite3.connect('audios.db')
c = conn.cursor()

# ELEGIR DIRECTORIO

#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/ACTO 1/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/ACTO 1 OK/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/ACTO 2/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/ATO 2 OK/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/04 - EL VIAJE DEL SIRIO/SIRIO V1/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/CRUZ DEL SUR BAFICI/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/EL CRUCERO DE LO IMPREVISTO/Audio Files'
#directorio = '/media/nofi/SONIDO/EL NAVEGANTE SOLITARIO/LOS CUARENTA BRAMADORES BAFICI/Audio Files'
#pelicula = 'El Navegante Solitario'




# CREAR TABLA SQLite CON FORMA: NOMBREARCHIVO (STRING), FORMATO (wav, aiff, mp3), DURACIÓN, FECHACREACION, PELICULA

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS audios(nombre TEXT, tam INTEGER, creacion REAL, directorio TEXT, "
              "pelicula TEXT)")

create_table()


def data_entry(nombre, tam, creacion, directorio, pelicula):
    c.execute("INSERT INTO audios VALUES(?, ?, ?, ?, ?)", (nombre, tam, creacion, directorio, pelicula))




# ENUMERAR UNO POR UNO LOS ARCHIVOS, CREANDO UN ROW PARA CADA UNO


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

with os.scandir(directorio) as dir_contents:
    for entry in dir_contents:
        nombre = entry.name
        if nombre[:2] == '._':
            print("archivo fantasma")
        else:
            info = entry.stat()
            tam = info.st_size
            creacion = info.st_ctime
            print(nombre, tam, creacion)
            data_entry(nombre, tam, creacion, directorio, pelicula)
            # print(datetime.fromtimestamp(creacion))

conn.commit()
c.close()
conn.close()