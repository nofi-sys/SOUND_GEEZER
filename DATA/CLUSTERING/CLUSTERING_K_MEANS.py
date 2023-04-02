import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


# Función para calcular la matriz de similitud
def compute_similarity_matrix(names):
    n = len(names)
    similarity_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            similarity = fuzz.token_set_ratio(names[i], names[j]) / 100
            similarity_matrix[i, j] = similarity
            similarity_matrix[j, i] = similarity

    return similarity_matrix


# Cargar datos del CSV
def load_data(file_path):
    df = pd.read_csv(file_path)
    audio_names = df['nombre_audio'].values
    return audio_names


# Aplicar K-means a la matriz de similitud
def apply_kmeans(similarity_matrix, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(similarity_matrix)
    return labels


# Ejecución principal del script
if __name__ == '__main__':
    # Cambia 'audio_data.csv' por el nombre real de tu archivo CSV
    file_path = r'/DATA/audios_a_categoria_LIMPIAR - DLG.csv'
    audio_names = load_data(file_path)

    similarity_matrix = compute_similarity_matrix(audio_names)

    # Elige el número de clusters que deseas encontrar
    n_clusters = 5
    cluster_labels = apply_kmeans(similarity_matrix, n_clusters)

    # Muestra los resultados
    for i in range(n_clusters):
        print(f'Cluster {i + 1}:')
        for name, label in zip(audio_names, cluster_labels):
            if label == i:
                print(f'  {name}')
        print()
