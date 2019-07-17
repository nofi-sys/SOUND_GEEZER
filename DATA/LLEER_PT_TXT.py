import pickle

archivo = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/ESA/DATA/PT/MULLER.ACTO 1 post LOGIC.ptx.txt'


with open(archivo, 'rb') as f:
    x = pickle.load(f)

print(x)
