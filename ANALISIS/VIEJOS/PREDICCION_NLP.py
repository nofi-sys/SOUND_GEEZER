import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Cargar los datos en un DataFrame de Pandas
df = pd.read_csv('/DATA/audios_y_categoria_track.csv')

# Eliminar las filas con valores NaN
df = df.dropna()

# Eliminar caracteres especiales, símbolos, espacios en blanco y caracteres no ASCII de los nombres de audio
def clean_string(string):
    # Eliminar caracteres especiales, símbolos y espacios en blanco
    string = re.sub(r'[^a-zA-Z0-9_]', '', string).replace(' ', '_')
    # Eliminar caracteres no ASCII
    string = re.sub(r'[^\x00-\x7F]', '', string)
    # Asegurar que el nombre de audio tenga una longitud mínima
    if len(string) < 5:
        string = string + '_' * (5 - len(string))
    # Devolver el nombre de audio limpio
    return string

df['nombre_audio'] = df['nombre_audio'].apply(clean_string)

# Dividir el contenido de cada celda de la columna "nombre_audio" en una lista de palabras
df['nombre_audio'] = df['nombre_audio'].apply(lambda x: x.split())

# Eliminar stopwords y lematizar las palabras
stop_words = set(stopwords.words('spanish'))
lemmatizer = WordNetLemmatizer()

def preprocess(words):
    # Eliminar stopwords
    words = [word for word in words if word not in stop_words]
    # Lematizar las palabras
    words = [lemmatizer.lemmatize(word) for word in words]
    # Devolver la lista de palabras preprocesadas
    return words

df['nombre_audio'] = df['nombre_audio'].apply(preprocess)

# Unir las palabras de cada lista en una cadena de texto
df['nombre_audio_string'] = df['nombre_audio'].apply(lambda x: ' '.join(x))

# Crear una matriz de frecuencia de términos (TF-IDF)
tfidf = TfidfVectorizer()
X = df['nombre_audio_string']

# Dividir los datos en un conjunto de entrenamiento y un conjunto de prueba
X_train, X_test, y_train, y_test = train_test_split(X, df['categoria'], test_size=0.2)


# Entrenar un modelo de clasificación
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluar el rendimiento del modelo
score = model.score(X_test, y_test)
print(f'Accuracy: {score:.2f}')

# Predecir la categoría de nombres de audio
def predict_category(audio_name):
    # Limpiar el nombre de audio y crear una matriz de frecuencia de términos (TF-IDF)
    audio_name = clean_string(audio_name)
    audio_name = [preprocess(audio_name.split())]
    X = tfidf.transform(audio_name)
    # Predecir la categoría del nombre de audio
    prediction = model.predict(X)[0]
    return prediction

prediction = predict_category('AMB PASILLO LARGO MS.L.wav')
print(f'Categoría del nombre de audio: {prediction}')
