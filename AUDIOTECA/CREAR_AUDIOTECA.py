import os
from pathlib import Path

ESTRUCTURA_AUDIOTECA = {
    'HUMANO': ['VOZ', 'SILBIDO', 'RESPIRACIÓN', 'LOCOMOCIÓN', 'DIGESTIÓN', 'MANOS', 'CORAZÓN', 'OTOACÚSTICO',
               'GRUPALES'],
    'ANIMAL': ['DOMÉSTICOS', 'TRABAJADORES', 'SALVAJES'],
    'NATURAL': ['VIENTO', 'TORMENTA', 'AGUA', 'FUEGO'],
    'MUSICAL': ['INSTRUMENTO', 'GÉNERO', 'CONCEPTO', 'ROL', 'MOOD'],
    'COSAS': ['VEHÍCULOS', 'MOTORES', 'DOMÉSTICOS', 'CAMPANAS', 'ALARMAS', 'MECANISMOS', 'HERRAMIENTAS', 'EXPLOSIONES',
              'MADERA', 'VIDRIO', 'LÍQUIDO', 'MISCELANEA', 'IMPACTO ESPECÍFICO'],
    'AMBIGUOS': ['IMPACTO GENERAL', 'CONTACTO CON SUPERFICIE', 'ESTRUCTURA DEFORMABLE', 'ONOMATOPEYA', 'SILENCIO',
                 'OTROS'],
    'FÁCTICOS': ['ENTORNO', 'RUIDO', 'REPRODUCCIÓN'],
    'SIN CLASIFICAR': []}


def crearAudioteca(path=str(Path.home()), nombre='AUDIOTECA', estructura=ESTRUCTURA_AUDIOTECA):
    # SI NO EXISTE, CREAR CARPETA LLAMADA AUDIOTECA
    dir = path + '/' + nombre
    if not os.path.exists(dir):
        os.makedirs(dir)

    # ITERAR POR ELEMENTOS DE ESTRUCTURA_AUDIOTECA

    for genero, tipos in estructura.items():

        # CREAR CARPETA CON NOMBRE CLAVE (ie: 'HUMANO')
        dirGen = dir + '/' + genero
        if not os.path.exists(dirGen):
            os.makedirs(dirGen)

        # DENTRO DE CADA CARPETA, CREAR UNA CARPETA PARA CADA ELEMENTO

        for tipo in tipos:
            dirTipo = dirGen + '/' + tipo
            if not os.path.exists(dirTipo):
                os.makedirs(dirTipo)


crearAudioteca()