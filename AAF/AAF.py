import aaf
from DIALOGOS.DETECCION_VOZ import *
import
import os

from GENERAL.AUDIO import *
from ANALISIS.CLASIFICAR import *

#HEREDA MÉTODOS DE CLASIFICACIÓN
class AAF(Clasificar):

    def __init__(self, archivo = "40 BRAMADORES INTRO.aaf"):

    #ABRIR AAF
        self.path = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/SAMPLES/NAVEGANTE/'
        self.archivo = self.path + archivo

        self.f = aaf.open(self.archivo, "r")

        # get the main composition
        self.comp = self.f.storage.toplevel_mobs()[0]

        # print the name of the composition
        print ('ABRIENDO COMPOSICIÓN: ' + self.comp.name)

    #CREAR AAF PARA OUTPUT
        archivo, extension = os.path.splitext(archivo)
        self.archivoNuevo =  self.path + archivo + ' ESA' + extension
        print('arch ', self.archivoNuevo)

    # ORDENAR AAF

        self.audios = []
        self.tracks = []
        self.ordenarAAF()


    def ordenarAAF(self):

    #NAVEGAR EL AAF Y PONER AUDIOS EN LISTA self.audios EN ORDEN POR TC:
    #CADA NUEVO OBJETO AUDIO QUE SE AGREGUE SERÁ CLASIFICADO UTILIZANDO
    #EL NOMBRE DE ARCHIVO

        for slot in self.comp.slots():
        # CADA comp.slots.segment ES UN Track:
            track = slot.segment
            print('TRACK:' , track.class_name)
            #  media_kind: DataDef_Picture, _Sound o _Timecode
            if track.media_kind == 'DataDef_Picture':
                self.outTrack(slot)

            elif track.media_kind == 'DataDef_Sound':

                # input_segments son regiones de audio
                for audio in track.input_segments():
                    # cada una con componentes
                    for c in audio.components():

                        #de distinta clase:
                        # OperatoionGroup: un bloque de segmentos agrupados,
                        # audios, transiciones, vacíos (fillers)
                        if c.class_name == 'OperationGroup':

                            for audio in c.input_segments():
                                #ACÁ BUSCAMOS LA REFERENCIA AL ARCHIVO DE SONIDO
                                self.nuevo_audio(audio)
                                print("AUDIO: ", audio.resolve_ref().name)
                                print("START TIME: ", audio.source_ref.start_time)
                                print("DURACION: ", audio.length)

                        #o pueden ser directamente fragmentos de audio:
                        #SourceClip
                        elif c.class_name == 'SourceClip':
                            print("SourceClip", c.source_ref.start_time)
                            print("AUDIO", c.resolve_ref().name)
                            print("offset: ", c.source_ref.offset_to_tc())

                        else:
                        #por las dudas que haya clases desconocidas
                            print(c.class_name)
                            print("DURACION: ", c.length)

    #CON LA LISTA COMPLETA, CREAR TRACKS



    #CREAR TRACKS. SI DOS REGIONES CON MISMA BANDERA (EJ: DIÁLOGOS) SE SUPERPONEN,
    #CREAR UN TRACK PARA CADA UNO. ORGANIZAR EN DAMERO. CAÑA + CORBATEROS.
    #PERO PARA LOGRAR ESO, PRIMERO DEBEMOS CLASIFICAR.

    #TAREAS DE CLASIFICACIÓN:

    #CLASIFICAR POR NOMBRE (hecho al crear instancia de Audio)

    #RECONOCER DIÁLOGOS: lo que tenga voces nítidas es un DIÁLOGO.

    def reconocerDIALOGOS(self, archivo, frame = 20, agresividad = 3):
        eventos = eventos_voz(archivo, frame, agresividad)



    #RECONOCER MUSICA

    #RECONOCER FX

    #RESOLVER EXCEPCIONES (EJ, MÚSICA CON VOZ). PUEDE SER CON SUPERVISIÓN HUMANA.

    #TERMINAR HACIENDO UN OUTPUT CON crearTrack()

    def nuevo_audio(self, audio):

        n_audio = Audio(audio.source_ref, audio.source_ref.start_time, audio.lenght)

        #ITERAR POR LISTA DE AUDIOS COMPARANDO EL START TIME CON EL DE
        # audio (enviado como argumento a esta función) Y UBICAR EL AUDIO
        #DE MANERA QUE QUEDEN EN ORDEN SEGUN TIMECODE DE INICIO
        for n, a in enumerate(self.audios):
            if n_audio['in'] >= a['in'] or n_audio['in'] == None:
                self.audios.insert(n, n_audio)

    def outTrack(self, slot):


        #UNA VEZ CREADO EL OBJETO TRACK, CREAR TRACK EN AAF EN BASE AL OBJETO
        print(self.archivoNuevo)
        out = aaf.open(self.archivoNuevo, "w")
        mob = out.create.MasterMob("Output")
        s = out.create.TimelineMobSlot()
        s.append_new_timeline_slot(slot)
        out.storage.add_mob(mob)
        #out.storage.add_mob(s)
        out.save()

if __name__ == '__main__':
    aaf = AAF()