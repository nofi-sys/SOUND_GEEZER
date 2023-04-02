from ANALISIS.CLASIFICAR import *

class Audio(Clasificar):

    def __init__(self, referencia, inicio = 0, largo = -1, h5 = None):

        #el Archivo de audio al que hace referencia nuestro objeto
        self.ref = referencia
        self.inicio = inicio
        self.out = inicio + largo
        self.transicion = Transicion

        #cambiar, que tag nombre ext y tipo se definanan en el método, no mediante return
        #CLASIFICAR POR NOMBRE debería devolver TAG, NOMBRE VALIDO, EXTENSION y TIPO
        self.CLASIFICAR_POR_NOMBRE(referencia)

        if h5 == None:
            self.PREPROCESAR_AUDIO(referencia)

        self.CLASIFICAR_POR_AUDIO(self.tag, self.nombreValido, self.ext, self.tipo)

class Transicion():

    def __init__(self, input = 0, out = 0):

        self.tipo  = ''
        self.input = input
        out   = out
