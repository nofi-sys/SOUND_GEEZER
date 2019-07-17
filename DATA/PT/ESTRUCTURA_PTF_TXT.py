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


# ABRIR BASE DE DATOS

# LEER LISTA DE TXT, IR ABRIENDO UNO POR UNO

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

# SI SE ENCUENTRA CON 'Audio file (WAV#) @ offset, length:'

# ABRIR TABLA AUDIOS
# INFO EN AUDIOS: NOMBRE, DURACIÓN

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

