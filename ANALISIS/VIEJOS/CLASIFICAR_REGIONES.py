import sqlite3
# TRACK(pelicula_id INTEGER, nombre TEXT,tag_id INTEGER, id INTEGER PRIMARY KEY, acto TEXT, FOREIGN KEY (pelicula_id) REFERENCES PELICULA (id), FOREIGN KEY (tag_id) REFERENCES TAG (id) ) ")
# AUDIO(id INTEGER PRIMARY KEY, nombre TEXT, duracion INTEGER)")
# REGION(id INTEGER PRIMARY KEY,nombre_audio TEXT, nombre_track TEXT, audio_id INTEGER, track_id INTEGER, into_track INTEGER,into_sample INTEGER, duracion INTEGER, FOREIGN KEY (audio_id) REFERENCES AUDIO (id), FOREIGN KEY (track_id) REFERENCES TRACK (id))")

DATABASE = '/home/nofi/DESARROLLO/ESA/DATA/ptfiles.db'

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

audios = {}
tracks = {}

# LEER REGIONES (REGION_ID, NOMBRE TRACK, NOMBRE AUDIOS)
for row in c.execute('SELECT id, nombre_audio, nombre_track, pelicula_id FROM REGION '):


    nombre = row[1]
    pelicula_id = row[3]
    audios[row[1]] = (row[0], row[3])
    tracks[row[2]] = (row[0], row[3])

    # LEER AUDIO (AUDIO_ID, NOMBRE_AUDIO)
for audio in audios:
    region_id = audios[audio][0]
    pelicula_id = audios[audio][1]
    audio_id = c.execute('SELECT id FROM AUDIO WHERE nombre = ? AND pelicula_id = ?', (audio, pelicula_id))
    audio_id = audio_id.fetchone()
    try:
        audio_id = audio_id[0]
    except:
        audio_id = None
    #print(audio_id)
    c.execute("UPDATE REGION SET audio_id = ? WHERE id = ?", (audio_id, region_id))

for track in tracks:
    region_id = tracks[track][0]
    pelicula_id = tracks[track][1]
    track_id = c.execute('SELECT id FROM TRACK WHERE nombre = ? AND pelicula_id = ?', (track, pelicula_id))
    track_id = track_id.fetchone()
    try:
        track_id = track_id[0]
    except:
        track_id = None

    #print(audio_id)
    c.execute("UPDATE REGION SET track_id = ? WHERE id = ?", (track_id, region_id))


conn.commit()

#    print(audio_id.fetchone ())

#else: pass
   # audio_id = c.fetchone()
    #print(audio_id)
    #print(row)
    # LEER TRACKS (TRACK_ID, NOMBRE_TRACK

# ENUMERAR UNA POR UNA LAS REGIONES, BUSCAR AUDIO POR NOMBRE_AUDIO, ENCONTRAR AUDIO_ID

# HACER LO MISMO CON NOMBRE_TRACK Y TRACK_ID