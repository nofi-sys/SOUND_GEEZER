import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.cluster import SpectralClustering
from sklearn.metrics.pairwise import rbf_kernel
from tqdm import tqdm
from sklearn.cluster import DBSCAN


# Cargar datos del CSV
def load_data(file_path, max_length=50):
    df = pd.read_csv(file_path)
    # Filtrar nombres de archivo basados en la longitud máxima
    audio_names = df['nombre_audio'].apply(lambda x: x if isinstance(x, str) and len(x) <= max_length else None).dropna().values
    return audio_names

# Preprocesar texto y entrenar el modelo Word2Vec


def create_word2vec_model(audio_names, vector_size=100, window=5, min_count=1, workers=4, epochs=100):
    # Tokenizar los nombres de archivo
    tokenized_names = [str(name).split() if isinstance(name, str) else [] for name in audio_names]

    # Crear y entrenar el modelo Word2Vec
    print("Creando y entrenando el modelo Word2Vec...")
    model = Word2Vec(sentences=tokenized_names, vector_size=vector_size, window=window, min_count=min_count, workers=workers, epochs=epochs)

    return model

# Convertir nombres de audio en vectores utilizando el modelo Word2Vec
def names_to_vectors(audio_names, word2vec_model):
    audio_vectors = []

    for name in audio_names:
        # Divide el nombre en palabras y obtén los vectores correspondientes
        words = name.split()
        word_vectors = [word2vec_model.wv[word] for word in words if word in word2vec_model.wv]

        # Si no hay vectores de palabras, crea un vector de ceros
        if not word_vectors:
            vector = np.zeros(word2vec_model.vector_size)
        else:
            vector = np.mean(word_vectors, axis=0)

        audio_vectors.append(vector)

    return np.array(audio_vectors)

from sklearn.cluster import OPTICS

from tqdm.auto import tqdm
import time

def apply_clustering(audio_vectors):
    # Parámetros para OPTICS
    max_eps = 0.5
    min_samples = 5

    # Crear una barra de progreso aproximada
    pbar = tqdm(total=100, desc="Aplicando OPTICS", ncols=100)

    # Aplicar OPTICS
    print("Aplicando OPTICS...")
    clustering = OPTICS(max_eps=max_eps, min_samples=min_samples).fit(audio_vectors)

    # Actualizar y cerrar la barra de progreso aproximada
    pbar.update(100)
    pbar.close()

    return clustering.labels_

# Guardar los resultados en un archivo CSV
def save_results_to_csv(audio_names, cluster_labels, output_file):
    result_df = pd.DataFrame({'nombre_audio': audio_names, 'cluster': cluster_labels})
    result_df.to_csv(output_file, index=False)

# Ejecución principal del script
if __name__ == "__main__":
    # Cargar datos
    file_path = r'/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/audios_a_categoria_LIMPIAR - DLG.csv' #
    #file_path = r'/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/audios_y_categoria_track.csv' # Reemplaza esto con la ruta de tu archivo CSV
    audio_names = load_data(file_path)

    # Preprocesar texto y convertir nombres en vectores
    word2vec_model = create_word2vec_model(audio_names)
    audio_vectors = names_to_vectors(audio_names, word2vec_model)

    # Aplicar clustering
    labels = apply_clustering(audio_vectors)

    # Crear un DataFrame de pandas con los resultados
    result_df = pd.DataFrame({"nombre_audio": audio_names, "cluster": labels})

    # Guardar el DataFrame en un archivo CSV
    output_file = 'resultado_clustering_2.csv'  # Reemplaza esto con la ruta de tu archivo de salida
    result_df.to_csv(output_file, index=False)
