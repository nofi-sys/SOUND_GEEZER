import sqlite3


conn = sqlite3.connect("/home/nofi/DESARROLLO/ESA/DATA/ptfiles.db")
c = conn.cursor()
nlp = spacy.load('es_core_news_sm')
nlp.max_length = 1500000

def extraerTag(nombre):
    """RECIBE NOMBRE DE ARCHIVO Y DEVUELVE TAG + NOMBRE  """
   #TODO: FALTA RECONOCER CUANDO LA PRIMERA PALABRA NO ES UN TAG.
   #LA IDEA MÁS INGENUA ES CREAR UNA LISTA DE TAGS
    nombre.replace('.', ' ')
    nombre.replace('_', ' ')
    nombre.replace('-', '.')
    tag = nombre.split(' ', 1)[0]
    for letra in tag:
        if letra == '.':
            pass


    #tag = tag[: tag.find('.')]

    return tag

c.execute('SELECT * FROM TRACK')
tracks = c.fetchall()
tracks = [track, id for _, track, _, id, _ in tracks]
tags = []

# SI EL ANTERIOR TRACK TAGUEADO Y EL PRÓXIMO TRACK TAGUEADO TIENEN EL MISMO TAG,
# TODOS LOS TRACKS INTERMEDIOS SON TAGUEADOS COMO PERTENECIENTES A ESE
# PERO ANTES HACER UN CHEQUEO DE SEGURIDAD.

for track, id in tracks:
     pass
