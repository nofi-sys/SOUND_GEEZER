import sqlite3


# DISTINGUIR ENTRE BLOQUES HOMOGÉNEOS

TIPOS_BLOQUE = ['ABC', 'NUM', 'SIM']

# ALFABETICOS
ABC = 0
# if x in ABC:
#    bloque_actual = ABC
# NUMÉRICOS
NUM = 1
# SIMBÓLICOS
SIM = 2


class Estructura:

    def __init__(self, texto='MVI_1121'):
        self.texto = texto
        self.partes = ['']
        self.forma_simple = []
        self.forma_compleja = self.analisisMorfologico(self.texto)

    def analisisMorfologico(self, texto):
        forma = []
        parte = 0
        letra_anterior = None
        for letra in texto:
            if letra.isalpha():
                if letra_anterior == None:
                    self.forma_simple.append(ABC)
                    letra_anterior = ABC

                if letra_anterior == ABC:
                    self.partes[parte] += letra
                else:
                    parte += 1
                    self.partes.append(letra)
                    self.forma_simple.append(ABC)
                letra_anterior = ABC
                forma.append(ABC)

                #print(letra, ' es ', 'LETRA')
            elif letra.isdigit():
                if letra_anterior == None:
                    self.forma_simple.append(NUM)
                    letra_anterior = NUM
                if letra_anterior == NUM:
                    self.partes[parte] += letra
                else:
                    parte += 1
                    self.partes.append(letra)
                    self.forma_simple.append(NUM)
                letra_anterior = NUM
                forma.append(NUM)

                #print(letra, ' es ', 'NUMERO')
            else:
                if letra_anterior == None:
                    self.forma_simple.append(SIM)
                    letra_anterior = SIM
                if letra_anterior == SIM:
                    self.partes[0] += letra
                else:
                    parte += 1
                    self.partes.append(letra)
                    self.forma_simple.append(SIM)
                letra_anterior = SIM
                forma.append(SIM)

                #print(letra, ' es ', 'SIMBOLO')
        self.forma_simple = tuple(self.forma_simple)
        return tuple(forma)


class Morfologia:

    def __init__(self):

        self.formas = {
            'simples':{},
            'complejas':{},
            'partes':{}
        }

        self.comparar()

    def comparar(self):

        for item in self.baseDeDatos():
            estructura = Estructura(item[0])
            print(estructura.partes, estructura.forma_simple, estructura.forma_compleja)
            if estructura.forma_simple in self.formas['simples']:
                self.formas['simples'][estructura.forma_simple] +=1
            else:
                self.formas['simples'].update({estructura.forma_simple : 1})

    def baseDeDatos(self):
        datos = []
        # abrir base de datos
        conn = sqlite3.connect('ptfiles.db')
        c = conn.cursor()
        # seleccionar todos los nombres de archivo
        c.execute('SELECT nombre_audio FROM REGION')
        # append nombres de archivo a lista datos
        for nombre in c.fetchall():
            datos.append(nombre)
        return datos

morfologia = Morfologia()
print(morfologia.formas['simples'])
# estructura = Estructura()
# print(estructura.forma)
# print(estructura.partes)
# print(estructura.forma_simplificada)
