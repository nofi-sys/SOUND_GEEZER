

#La idea es la siguiente: cuando se crea un objeto Tipo (generalmente al
#comienzo del trabajo en un proyecto, típicamente, cargando un AAF y creando
#un objeto para cada audio). Se envía sin clasificar, creando un tipo = Tipo,
#clasificándolo primero por nombre, luego por features de audio y otorgándole
#finalmente un tipo. Ej: DIRECTO. Al otorgarle un tipo, se vuelve a inicializar
#el objeto, pasando el tipo como argumento.




DIALOGOS = 'HABLADOS'
SONO =  'FOLEY'
ESCENA = 0
PLANO = 1
X = 2

NORM_EXCEPTIONS = {
    "S-S": "SONIDO SOLOS",
    "SX": "SONIDO SOLOS",
    "AMB": "AMBIENTE",
    "AX": "AMBIENTE",
    "DIR": "DIRECTO",
    "DX": "DIRECTO",
    "DUB": "DOBLAJE"
}

duracionTipo = ['ESCENA', 'PLANO', 'X']

#ESTRUCTURA TIPO

tipos = {
         'HABLADOS' : {'subtipo': {'DIRECTOS':{'duracionTipo': duracionTipo[PLANO]}},
                       'DUBS':{'duracionTipo': duracionTipo[X]},
                       'S-S-H':{'duracionTipo': duracionTipo[X]}}, # S-S HABLADO
         'S-S': {'subtipo': {'FOLEY': {'duracionTipo': duracionTipo[X]},
                             'WILDTRACK': {'duracionTipo': duracionTipo[X]},
                             'SONO':{'duracionTipo': duracionTipo[X]},
                             'S-S':{'duracionTipo': duracionTipo[X]}}},
         'AMBS': {'duracionTipo': duracionTipo[ESCENA]},
         'FX': {'duracionTipo': duracionTipo[X]},
         'MUSICA': {'duracionTipo': duracionTipo[X]}
         }

TAG_LISTA = ['S-S', 'S/S', 'SONO', 'BIBLIO', 'AMBIENTE', 'AMB', 'DUB', 'FX']


class Tipo():

    def __init__(self, tipo = None, subtipo = None):

        self.tipo = tipo
        #print(self.tipo)
        self.subtipo = subtipo
        #print(self.subtipo)
        self.duracionFundido = 2


        #INTENTAR ACCEDER A CARACTERÍSTICAS POR TIPO, SI ES IMPOSIBLE,
        #ACCEDER POR SUBTIPO

        try:
            self.duracionTipo = tipos[tipo]['subtipo'][subtipo]['duracionTipo']
        except:
            self.duracionTipo = tipos[tipo]['duracionTipo']

       # print(self.duracionTipo)

DIRECTOS = (DIALOGOS, 'DIRECTOS')
AMB = Tipo('AMBS')
SS = Tipo('S-S', 'SONO')

class Nombre():

    """ESTRUCTURA TIPICA DE UN NOMBRE DE ARCHIVO"""

    def __init__(self, tipo = None,
                 clave = None, extrinsicas = None, intrinsecas = None):

        tipo = tipo
        clave = clave
        extrinsicas = extrinsicas
        intrinsecas = intrinsecas