import pickle

AUDIOTECA_CLAVES = {
    'HUMANO': {'VOZ': {'DUB': 0},
               'SILBIDO': {},
               'RESPIRACIÓN': {'RESP': 0},
               'LOCOMOCIÓN': {'PASOS': 0,'CORRIDA': 0,'CAMINATA': 0,'PROCESION': 0},
               'DIGESTIÓN': {'ESTOMAGO': 0},
               'MANOS': {'PALMA': 0, 'APLAUSO': 0, 'PIÑA': 0, 'GOLPE': 0, 'APRETON': 0},
               'CORAZÓN':{'LATIDO': 0},
               'OTOACÚSTICO': {},
               'GRUPALES':{'MULTITUD': 0, 'ABUCHEO': 0, 'APLAUSOS': 0}
               },

    'ANIMAL': {'DOMÉSTICOS': {'PERRO': 0, 'GATO': 0, 'CANARIO': 0, 'LADRIDO': 0, 'MAULLIDO': 0, 'PIO': 0},
               'TRABAJADORES':{'CABALLO': 0, 'VACA': 0, 'BUEY': 0, 'TORO': 0, 'GANSO': 0, 'PAVO': 0},
               'SALVAJES':{'LOBO': 0, 'AULLIDO': 0, 'TIGRE': 0, 'LEON': 0, 'RUGIDO': 0}},
    'NATURAL': {'VIENTO':{}, 'TORMENTA':{}, 'AGUA':{'RIO': 0, 'MAR': 0, 'OLA': 0}, 'FUEGO':{}},
    'MUSICAL': {'INSTRUMENTO':{}, 'GÉNERO':{}, 'CONCEPTO':{}, 'ROL':{}, 'MOOD':{}},
    'COSAS': {'VEHÍCULOS':{'AUTO': 0, 'CAMION': 0, 'CAMIONETA': 0, 'TRACTOR': 0, 'MOTO': 0, 'CICLOMOTOR': 0, 'SCOOTER': 0 },
              'MOTORES':{}, 'DOMÉSTICOS':{'BICICLETA': 0, 'TRICICLO': 0,}, 'CAMPANAS':{}, 'ALARMAS':{}, 'MECANISMOS':{'PEDAL': 0, 'CADENA': 0}, 'HERRAMIENTAS':{'MARTILLO': 0, 'TORQUEADORA' : 0}, 'EXPLOSIONES':{'PETARDO': 0},
              'MADERA':{}, 'VIDRIO':{}, 'LÍQUIDO':{}, 'MISCELANEA':{}, 'IMPACTO ESPECÍFICO':{}},
    'AMBIGUOS': {'IMPACTO GENERAL':{}, 'CONTACTO CON SUPERFICIE':{}, 'ESTRUCTURA DEFORMABLE':{}, 'ONOMATOPEYA':{'UH': 0, 'SHH': 0}, 'SILENCIO':{},
                 'OTROS':{}},
    'FÁCTICOS': {'ENTORNO':{}, 'RUIDO':{}, 'REPRODUCCIÓN':{}},
    'SIN CLASIFICAR': {'SIN CLASIFICAR':{}}
}


raiz = '/home/nofi/AUDIOTECA/'


with open(raiz + 'CLAVES.pck', 'wb') as lista:
    pickle.dump(AUDIOTECA_CLAVES, lista)

#with open(raiz + 'CLAVES.pck', 'rb') as claves:
#    CLAVES = pickle.load(claves)

