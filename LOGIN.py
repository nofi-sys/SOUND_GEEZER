from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.app import App



import pickle
from shutil import copyfile

from usuario import *

#Config.set('kivy', 'keyboard_mode', 'managed')
#Config.write()

class Login(Screen):


    def crearUsuario(self):

        usuario = Usuario()


        # crear pickle para comunicación entre distintas utilidades de la suite.
        # El nombre del archivo es 'paciente.pickle' y cada vez que se usa la suite,
        # se sobreescribe.
        copyfile('DATA/usuario.pickle', 'DATA/usuario.bak')
        with open('DATA/' + usuario.archivo, 'wb') as arch:

            pickle.dump(usuario, arch)

        return


class Menu(Screen):
    font_s = 35
    pass

class Vocabulario (Screen):
    pass

class Esa(ScreenManager):
    pass

#suiteCognitiva = Builder.load_file("paula.kv")

class EsaApp(App):
    def Build(self):
        return Esa

EsaApp().run()