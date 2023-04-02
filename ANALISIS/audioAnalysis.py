import os

ARRIBA = False
ABAJO = True


class ANALISIS():

    def __init__(self):
        self.status = None

    def primeraVez(self,valor):
        if self.status == valor:
            return False
        else:
            self.status = valor
            return True

    def reconocimientoPorEnergia(self, FONDO, FIGURA, F, umbral = 0.001, archivo = 'Test.dsc'):

        #X = [[bool, str], bool]
        X = Descriptor(archivo)

        for frame in F[1, 400:700]:
            if frame < umbral:

                if self.primeraVez(ABAJO):
                    X.append([[FONDO.valor, FONDO.nombre], False])
                    #self.primeraVez.valor = not primeraVez

                else:
                    X.append([[], False])

            else:

                if self.primeraVez(ARRIBA):
                    X.append([[FIGURA.valor, FIGURA.nombre], True])
                    #primeraVez = not primeraVez
                else:
                    X.append([[], True])
        return X

class Descriptor():

    def __init__(self, archivo):
        self.fuente = archivo
        self.archivo, self.tipoFuente = os.path.splitext(archivo)
        self.archivo += '.dsc'
        self.crearArchivo(self.archivo)


    def crearArchivo(self, archivo, fraps = 24):

        pass



if __name__ == "__main__":

    descriptor = Descriptor("prueba.wav")