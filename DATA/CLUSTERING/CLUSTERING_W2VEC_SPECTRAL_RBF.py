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
def preprocess_and_train_word2vec(audio_names, embedding_size=100, window=5, min_count=1):
    # Tokenizar los nombres de audio
    tokenized_names = [str(name).split() for name in audio_names]

    # Entrenar el modelo Word2Vec
    model = Word2Vec(sentences=tokenized_names, vector_size=embedding_size, window=window, min_count=min_count, workers=4)

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

# Aplicar Spectral Clustering a los vectores de nombres de audio
def apply_spectral_clustering(audio_vectors, n_clusters, gamma=1.0):
    # Calcular la matriz de similitud RBF
    similarity_matrix = rbf_kernel(audio_vectors, gamma=gamma)

    # Aplicar Spectral Clustering
    clustering = SpectralClustering(n_clusters=n_clusters, affinity='precomputed', random_state=42)
    labels = clustering.fit_predict(similarity_matrix)

    return labels

def apply_clustering(audio_vectors):
    # Parámetros para DBSCAN
    eps = 0.5
    min_samples = 5

    # Aplicando DBSCAN
    print("Aplicando DBSCAN...")
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(audio_vectors)
    return clustering.labels_


# Guardar los resultados en un archivo CSV
def save_results_to_csv(audio_names, cluster_labels, output_file):
    result_df = pd.DataFrame({'nombre_audio': audio_names, 'cluster': cluster_labels})
    result_df.to_csv(output_file, index=False)

# Ejecución principal del script
if __name__ == '__main__':
    # Cambia 'audio_data.csv' por el nombre real de tu archivo CSV
    file_path = r'/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/audios_a_categoria_LIMPIAR - DLG.csv'
    audio_names = load_data(file_path)

    # Entrenar el modelo Word2Vec
    print("Entrenando el modelo Word2Vec...")
    word2vec_model = preprocess_and_train_word2vec(audio_names)

    # Convertir nombres de archivo en vectores
    print("Convirtiendo nombres de archivo en vectores...")
    audio_vectors = names_to_vectors(audio_names, word2vec_model)

    # Elige el número de clusters que deseas encontrar
    n_clusters = 5
    gamma = 1.0  # Ajusta el valor de gamma para la función RBF

    print("Aplicando Spectral Clustering...")
    cluster_labels = apply_spectral_clustering(audio_vectors, n_clusters, gamma)

    # Guardar los resultados en un archivo CSV
    output_file = 'clustering_results.csv'
    save_results_to_csv(audio_names, cluster_labels, output_file)
    print(f'Resultados guardados en {output_file}')
