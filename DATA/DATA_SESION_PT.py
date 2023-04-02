import subprocess
from subprocess import PIPE
import os
import shutil
import pickle
import tqdm

# ptformat = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/ESA/EXTRAS/ptformat-master/'
ptformat = '/home/nofi/DESARROLLO/PAQUETES/ptformat-master/'
carpetaSesionesPT = '/home/nofi/DESARROLLO/PAQUETES/ptformat-master/sesiones/'
dataDump = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/ESA/DATA/PT/'
#extensionesPT = ('ptx', 'ptf', 'pts')
extensionesPT = ('ptx')
#extensionesPT = ('ptf')

# ABRIR SESION PRO TOOLS E INSERTAR DATA EN BASE DE DATOS
def abrirsesionpt(archivopt):
    print ('ARCHIVO PT: ',archivopt)
    print([ptformat + './ptftool', archivopt])
    try:
        parsedData = tqdm (subprocess.run([ptformat + './ptftool', archivopt], stdout=PIPE, stderr=PIPE))
        print (parsedData)
        return parsedData
    except:
        pass

# ITERAR POR CARPETA DE SESIONES PT

for (dirpath, dirnombre, archivos) in os.walk(carpetaSesionesPT):

    for archivo in archivos:
        if archivo.endswith(extensionesPT):
            head, tail = os.path.split(dirpath)
            _, ext = os.path.splitext(archivo)
            nuevoArchivo = dataDump + tail + '.' + archivo + '.txt'
            archivotemp = dirpath + '/a' + ext

            print('ext ', ext, 'nuevoARchivo ', nuevoArchivo, 'archivotemp ',archivotemp )

            shutil.copy2(dirpath +'/'+ archivo,  archivotemp)
            data = abrirsesionpt(archivotemp)
            os.remove(archivotemp)
            f = open(nuevoArchivo, 'wb+')
            pickle.dump(data, f)
 #           print(nuevoArchivo)
            f.close()
