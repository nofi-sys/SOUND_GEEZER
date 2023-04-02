
filename = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/SAMPLES/8khz/Voz off 2.MP3_L.wav'

from io import BytesIO
from collections import namedtuple
import wave
import audioop
from argparse import ArgumentParser
from webrtcvad import Vad

AudioFrame = namedtuple("AudioFrame", "bytes, timestamp, duration")


def frame_generator(audio, frame_duration, sample_rate):
    """A generator to get audio frames of specific length in time.
    :param BytesIO audio: Audio data.
    :param int frame_duration: Frame duration in ms.
    :param int sample_rate: Audio sample rate in Hz.
    """
    n = int(sample_rate * (frame_duration / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield AudioFrame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def downsample(buf, outrate=16000):
    """Downsample audio. Required for voice detection.
    :param buf: Audio data buffer (or path to WAV file).
    :param int outrate: Output audio sample rate in Hz.
    :returns: Output buffer.
    :rtype: BytesIO
    """
    wav = wave.open(buf)
    inpars = wav.getparams()
    frames = wav.readframes(inpars.nframes)

    # Convert to mono
    if inpars.nchannels == 2:
        frames = audioop.tomono(frames, inpars.sampwidth, 1, 1)

    # Convert to 16-bit depth
    if inpars.sampwidth > 2:
        frames = audioop.lin2lin(frames, inpars.sampwidth, 2)

    # Convert frame rate to 16000 Hz
    frames, _ = audioop.ratecv(frames, 2, 1, inpars.framerate, outrate, None)

    # Return a BytesIO version of the output
    outbuf = BytesIO()
    out = wave.open(outbuf, "w")
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(outrate)
    out.writeframes(frames)
    out.close()
    outbuf.seek(0)
    return outbuf


def get_voice_events(filename, frame_dur, aggressiveness):
    """Evaluate the file for voice events.
    :param str filename:
    :param int frame_dur:
    :param int aggressiveness:
    """
    assert frame_dur in [10, 20, 30]
    assert aggressiveness in range(4)

    vad = Vad()
    vad.set_mode(args.aggressiveness)
    sample_rate = 16000
    frame_dur = args.frame_duration

    clip = downsample(filename, sample_rate).read()
    return [
        (frame_dur*n, vad.is_speech(frame.bytes, sample_rate))
        for n, frame in enumerate(frame_generator(clip, frame_dur, sample_rate))
    ]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--frame-duration", default=20, type=int,
                        help="Frame length in ms")
    parser.add_argument("-a", "--aggressiveness", default=1, type=int,
                        help="Voice detection aggressiveness")
    args = parser.parse_args()

    for filename in ["noise.wav", "speech.wav", "sfx.wav"]:
        print("Checking", filename)
        events = get_voice_events(filename, args.frame_duration, args.aggressiveness)
print(events)
class Dialogos():
    pass

#MÉTODOS BÁSICOS:


#USAR:
#audioSegmentation.speakerDiarization(fileName, numOfSpeakers, mtSize=2.0, mtStep=0.2, stWin=0.05, LDAdim=35, PLOT=False):

#RECONOCER CAÑA vs CORBATEROS

#PONER EN FASE --> RECONOCER VISUALMENTE
#              --> ANALIZAR AUDIO CHEQUEANDO FASE

#ANÁLISIS DEL NOMBRE DE ARCHIVO. NORMALIZAR A ESC-PLANO-TOMA SI ES POSIBLE

#AUDIO A TEXTO. SI ES POSIBLE, COTEJAR Y AYUDARSE CON GUION.

#ANALISIS VOCAL: SEPARAR VOCES DE ACTORES POR POR COLOR DE VOZ. HACERLO PRIMERO EN
#CORBATEROS (DONDE VA A HABER UNA IMPORTANTE DIFERENCIA DE PLANO ENTRE EL QUE TIENE
#EL CORBATERO Y LOS OTROS). USAR INFO DE CORBATEROS PARA SEGREAR CAÑA (SEGREGACIÓN
#DÉBIL).

#CREAR PERFIL DE HABLANTE PARA USO EN TODA LA PELÍCULA O EN PROYECTOS FUTUROS.

#CREAR REPRESENTACIÓN EN MINIATURA DE FRASES (TEXTO + DIBUJO ESQUEMATICO DE AUDIO
# + IDENTIDAD HABLANTE)

#ANALIZAR DIRECTOS EN BUSCA DE FRASES QUE NO SIRVAN (POR FUERA DE PLANO
#O POR RUIDO INVASIVO). PUNTUAR PRIMERO LA CAÑA FRASE A FRASE. EL PRIMER UMBRAL
#DETERMINA SI LA CAÑA SIRVE POR SÍ MISMA (ANALIZA COLOR DE VOZ, PLANO Y FONDO). SI
#LA CAÑA ESTÁ DEBAJO DEL PRIMER UMBRAL, CHEQUEAR EL CORBATERO Y PESAR COMBINACIÓN.
#SI ALGUNA FRASE QUEDA POR DEBAJO DEL SEGUNDO UMBRAL, BUSCAR REEMPLAZO.

#  ANALIZAR

#MÉTODOS COMPLEJOS:

#ENCONTRAR REEMPLAZOS
    #ENCONTRAR ALTERNATIVAS A TODA LA ESCENA (MÉTODO COSTOSO):
    #EN CARPETA DIRECTOS (O EN DIRECCIÓN ESPECÍFICA, O EN SELECCIÓN DE USUARIO ):
    #RECONOCER TODOS LOS DIRECTOS PARALELOS (TOMAS ALTERNATIVAS)
    #AYUDARSE CON NOMBRE DE ARCHIVO O POR HORA DE GRABACIÓN.
    #EN PRESELECCIÓN, TOKENIZAR Y COMPARAR CON DIRECTO (POR REPRESENTACIÓN EN
    #MINIATURA).
    #ARMAR GUION Y PROPONER REEMPLAZOS.
    #PUNTUAR OPCIONES POR PLANO, SINCRO Y FONDO.

    #ENCONTRAR ALTERNATIVA A FRASE SELECCIONADA. LO MISMO QUE ANTES PERO SÓLO CON
    #UN FRAGMENTO DEL DIRECTO.

    #OPCIÓN: USAR ARCHIVO ESPECÍFICO DE SONIDO SOLO.



#GRABAR DUBS --> DUB = REEMPLAZO SINTÉTICO

#ALGORITMO AUTOMÁTICO--> LOOP: DIÁLOGO A DOBLAR + SILENCIO PARA LA GRABACIÓN
    #                --> PUNTUAR OPCIONES POR SINCRO
    #                --> RECOMENDAR POSICIÓN DE MIC POR COMPARACIÓN DE PLANOS
