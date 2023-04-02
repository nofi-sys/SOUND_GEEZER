import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import re


# Cargar los datos en un DataFrame de Pandas
df = pd.read_csv('/DATA/audios_y_categoria_track.csv')

# Eliminar las filas con valores NaN
df = df.dropna()
df = df[df['categoria'] != 'XXX']

# Convertir los valores de la columna "nombre_archivo" a cadenas de texto válidas
df['nombre_audio'] = df['nombre_audio'].apply(str)

# Convertir los valores de la columna "nombre_archivo" a cadenas de texto válidas para el vectorizador
df['nombre_audio'] = df['nombre_audio'].apply(lambda x: x.replace(' ', '_'))

def clean_string(string):
    # Eliminar caracteres especiales, símbolos y espacios en blanco
    string = re.sub(r'[^a-zA-Z0-9_]', '', string).replace(' ', '_')
    # Eliminar caracteres no ASCII
    string = re.sub(r'[^\x00-\x7F]', '', string)
    # Asegurar que el nombre de archivo tenga una longitud mínima
    if len(string) < 5:
        string = string + '_' * (5 - len(string))
    # Devolver el nombre de archivo limpio
    return string

df['nombre_audio'] = df['nombre_audio'].str.lower()
df['nombre_audio'] = df['nombre_audio'].apply(clean_string)

# Mostrar los primeros 10 valores de la columna "nombre_archivo"
print(df['nombre_audio'].head(10))

# Convertir los valores de la columna "nombre_archivo" a números
#df['nombre_audio'] = pd.to_numeric(df['nombre_audio'])

# Separar las columnas "nombre_archivo" y "categoria" en dos variables diferentes
X = df['nombre_audio']
y = df['categoria']

# Dividir los datos en dos conjuntos de forma aleatoria, uno para entrenamiento y otro para prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Crear un vectorizador de frecuencias de términos (TF-IDF)
vectorizer = TfidfVectorizer()

# Vectorizar los nombres de archivo
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)



# Crear un modelo de regresión logística
model = LogisticRegression()

# Entrenar el modelo con el conjunto de entrenamiento
model.fit(X_train, y_train)

# Hacer predicciones con el conjunto de prueba
y_pred = model.predict(X_test)

from sklearn.metrics import precision_score, recall_score

# Calcular la precisión y el recall del modelo
precision = precision_score(y_test, y_pred, average='micro')
recall = recall_score(y_test, y_pred, average='micro')

# Mostrar el resultado
print(f'Precisión: {precision:.2f}')
print(f'Recall: {recall:.2f}')
