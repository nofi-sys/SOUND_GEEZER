import pandas as pd
import pickle

# Leer el archivo .csv y cargar los datos en un DataFrame
df = pd.read_csv('/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/audios_y_categoria_track.csv')

#NORMALIZAR
# Seleccionar la columna con los nombres de archivo
df['nombre_audio'] = df['nombre_audio'].str.lower()
df['nombre_audio'] = df['nombre_audio'].str.replace('.', ' ')
# df['nombre_audio'] = df['nombre_audio'].str.replace('-', ' ')
df['nombre_audio'] = df['nombre_audio'].str.replace('_', ' ')
# df['nombre_audio'] = df['nombre_audio'].str.replace(r'\d', '')

# Filtrar los valores NaN de la columna 'nombre_audio'
df = df[df['nombre_audio'].notnull()]

# Crear una lista de etiquetas
etiquetas = []

# Recorrer el DataFrame y extraer la primera palabra de cada nombre de archivo
for i in range(len(df)):
    etiqueta = df.iloc[i]['nombre_audio'].split()[0]
    etiquetas.append(etiqueta)

# Crear un diccionario con la frecuencia de cada etiqueta
frecuencias = {}
for etiqueta in etiquetas:
    if etiqueta in frecuencias:
        frecuencias[etiqueta] += 1
    else:
        frecuencias[etiqueta] = 1

# Establecer el umbral de frecuencia (entre 0.00 y 1.00)
umbral = 0.001

# Filtrar las etiquetas con frecuencia menor al umbral
etiquetas_filtradas = [etiqueta for etiqueta, frecuencia in frecuencias.items() if frecuencia/len(etiquetas) >= umbral]

# Imprimir la lista de etiquetas filtradas
print(etiquetas_filtradas)


# Abrir un archivo en modo de escritura binaria
with open('etiquetas.pickle', 'wb') as archivo:
  # Escribir el diccionario en el archivo
  pickle.dump(frecuencias, archivo)

# Crear una lista de categorías
categorias = ['CAM', 'S-S', 'AMB', 'DLG', 'MUS', '_']

# Crear un diccionario para almacenar la asignación de etiquetas a categorías
etiquetas_categorias = {}

# Recorrer cada etiqueta en etiquetas_filtradas
for etiqueta in etiquetas_filtradas:
  # Preguntar a qué categoría pertenece la etiqueta
  print(f'A qué categoría pertenece la etiqueta "{etiqueta}"? (ingrese un número)')
  for i, categoria in enumerate(categorias):
    print(f'{i}: {categoria}')
  # Leer la respuesta del usuario
  respuesta = input()
  # Asignar la etiqueta a la categoría seleccionada
  etiquetas_categorias[etiqueta] = categorias[int(respuesta)]

# Imprimir el diccionario de etiquetas a categorías
print(etiquetas_categorias)
