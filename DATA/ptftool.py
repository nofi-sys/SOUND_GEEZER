# SCRIPT DE PYTHON PARA TRANSFORMAR ARCHIVOS DE SESIÓN PRO TOOLS (ptx, ptf, pts)
# EN ARCHIVO .txt CON INFORMACIÓN MUY COMPLETA DE AQUELLA.

import subprocess
from subprocess import Popen, PIPE
import os
import shutil
import csv
import tqdm
import pickle

# INDICAR ARCHIVO A PROCESAR
ptformat = '/home/nofi/DESARROLLO/PAQUETES/ptformat-master/'
ptftool = './ptftool'
sesiones = '/home/nofi/DESARROLLO/PAQUETES/ptformat-master/sesiones/'
sesionesOk = '/home/nofi/DESARROLLO/PAQUETES/ptformat-master/sesionesOk/'
sesionesProcesadas = '/home/nofi/DESARROLLO/PAQUETES/ptformat-master/sesionesProcesadas/'
sesionesCSV = sesionesOk + 'sesionesPTFOriginales.csv'
dataDump = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/ESA/DATA/PT/'

ext = ['ptx', 'ptf', 'pts']

def procesarptf(archivo):
    texto = subprocess.run([ptformat + ptftool, archivo], stdout=PIPE, stderr=PIPE)
    return texto

# RECORRER CARPETA SESIONES Y, DE ENCONTRAR UN ARCHIVO PRO TOOLS, PROCESARLO 
def preprocesarPTFs():
    for root, dirs, files in os.walk(sesiones):
        
        for item, name in enumerate (files):
            peli = root.split(os.sep)[-1]
            extension = os.path.splitext(name)[-1]
            nuevoNombre = peli + '_' +str(item) + extension
            shutil.copy2(root + '/' + name, sesionesOk + nuevoNombre)
            with open(sesionesCSV, 'a', encoding='utf8') as csv_file:
                wr = csv.writer(csv_file, delimiter='|')
                wr.writerow([name, nuevoNombre])

def chequearProcesados():
    for root, dirs, files in os.walk(dataDump):
        archivosProcesados = files
    for root, dirs, files in os.walk(sesionesOk):
        archivosSesiones = files
        for archivo in archivosSesiones:
            if archivo + '.txt' in archivosProcesados:
                shutil.move(root + archivo, sesionesProcesadas)
                print('PROCESADOS REUBICADOS')

def crearTXT():
    for root, _, archivos in os.walk(sesionesOk):
        print(archivos)
        for archivo in archivos:
            nuevoArchivo = dataDump + archivo + '.txt'
            print(nuevoArchivo)
            parsedData = procesarptf(root + archivo)
            with open(nuevoArchivo, 'wb+') as f:
                pickle.dump(parsedData, f)
            print('OK')

chequearProcesados()
crearTXT()
chequearProcesados()