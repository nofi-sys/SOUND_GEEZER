from collections import defaultdict
import pickle

diccionario_inicial = {'01': '_', 'off': 'DLG', 'amb': 'AMB', 'aventuras': '_', 'cruz': '_', 'cufr': '_', 'a': '_', 'criolla': '_', 'chacarera': '_', 'voz': 'DLG', '40': '_', 'el': '_', 'ens': '_', 'audio': '_', 'inst': 'MUS', 'lass': '_', 's-s': 'S-S', 'sono': 'S-S', 'ss': 'S-S', 'wind': '_', 'la': '_', 'lf': '_', 'biblio': 'S-S', 'dub': 'DLG', 'ep3': '_', 'epiii': '_', 'musica': 'MUS', 'mvi': 'CAM', 'ped': '_', 'la301': '_', 'fx': 'S-S', 'auto': '_', 'ambneverland02fps': '_', 'ambiente': 'AMB', 'madre': '_', 'ss-': 'S-S', 'pasos': 'S-S', 'traffic': '_', 'water': '_', 'pampas': '_', 'laflor': '_', 'muller': '_', '84': '_', '86': '_', '101': '_', 'acto': '_', 'vo': 'DLG', '68': '_', 's': 'S-S', '16feb': '_', '1': '_', '2': '_', 'e': '_', 'carlini': '_', 'marambio': '_', 'parche': '_', 'a2': '_', 'mullerkcta': '_', 'r26': '_', '080125-000': '_', 'muller120t': '_', '71': '_', 'mullerptom': '_', 'sspasosasfaltozapatillasnoch': '_', 'punch': '_', 'eservic': '_', 'casterman': '_', '001': '_', '002': '_', 'casa': '_', 'zoom0028': '_', '235262': '_', 'viaje': '_', '23': '_', 'd': '_', 'teatro': '_', 'e28p01': '_', 'luis': '_', 'marta': '_', '92847': '_', 'agente50esc13': '_', 'h2e28p3': '_', '104003': '_', 'e36p7': '_', 'e2p2': '_', 'a01': '_', 'e15p1': '_', 'e28p5a': '_', 'e36p5': '_', 'e31p1s': '_', 'america': '_', '238675': '_', 'clip': '_', 'mt13': '_', 'loro': '_', 'saga': '_', '58-2-2': '_', 'las': '_', 'col': '_', '02-cuarentabramadoresv2': '_'}
# Crear un diccionario vacío con listas vacías como valores por defecto
categorias = defaultdict(list)

# Recorrer el diccionario inicial
for palabra, categoria in diccionario_inicial.items():
  # Agregar la palabra a la lista de la categoría correspondiente
  categorias[categoria].append(palabra)

categorias.pop('_')

# Imprimir el diccionario final
print(categorias)

# Guardar el diccionario final en un archivo pickle

with open('categorias.pkl', 'wb') as f:
  pickle.dump(categorias, f)
