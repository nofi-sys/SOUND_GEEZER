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
        self.forma_simple = str(self.forma_simple)
        return tuple(forma)


class Morfologia:

    def __init__(self):

        self.formas = {
            'simples': self.baseDatosEstructuras_S(),
            'complejas':{},
            'partes':{}
        }

        #self.comparar()
        #self.crearTablaEstructura()

    def comparar(self):

        for item in self.baseDatosRegiones():
            estructura = Estructura(item[0])
            #print(estructura.partes, estructura.forma_simple, estructura.forma_compleja)
            if estructura.forma_simple in self.formas['simples']:
                self.formas['simples'][estructura.forma_simple] +=1
            else:
                self.formas['simples'].update({estructura.forma_simple : 1})

    def correlacionar(self):
        #print(self.baseDatosEstructuras_S())
        #print("formas",self.formas['simples'])

        for item in self.baseDatosRegiones():
            estructura = Estructura(item[0])
            print("item ",item[0], " id ", item[1])
            print("id estructura: ", self.formas['simples'][estructura.forma_simple])


    def crearTablaEstructura(self):

        self.comparar()
        lista_estructuras_simples = sorted(self.formas['simples'].items(), key=lambda x: x[1])
        print(lista_estructuras_simples)
        conn = sqlite3.connect('ptfiles.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS ESTRUCTURA_S(id INTEGER PRIMARY KEY, forma TEXT, cantidad INTEGER)")
        for estructura in reversed(lista_estructuras_simples):
            print(estructura)
            c.execute("INSERT INTO ESTRUCTURA_S (forma, cantidad) VALUES (?, ?)", (str(estructura[0]), estructura[1]))
        conn.commit()

    def baseDatosRegiones(self):
        datos = []
        # abrir base de datos
        conn = sqlite3.connect('ptfiles.db')
        c = conn.cursor()
        # seleccionar todos los nombres de archivo
        c.execute('SELECT nombre_audio, id FROM REGION')
        # append nombres de archivo a lista datos
        for nombre, id in c.fetchall():
            datos.append([nombre, id])
        return datos

    def baseDatosEstructuras_S(self):
        formas = {}
        # abrir base de datos
        conn = sqlite3.connect('ptfiles.db')
        c = conn.cursor()
        # seleccionar todos los nombres de archivo
        c.execute('SELECT forma, id FROM ESTRUCTURA_S')
        # append nombres de archivo a lista datos
        for forma, id in c.fetchall():
            formas.update ({forma: id})
        return formas

morfologia = Morfologia()
morfologia.correlacionar()
#print(morfologia.formas['simples'])
# estructura = Estructura()
# print(estructura.forma)
# print(estructura.partes)
# print(estructura.forma_simplificada)
