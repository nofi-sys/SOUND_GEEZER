import pandas as pd

def clean_dataset(input_csv, output_clean_csv, output_noise_csv):
    # Leer el archivo CSV de entrada
    data = pd.read_csv(input_csv)

    # Separar los datos en ruido y otros clusters
    noise_data = data[data['cluster'] == -1]
    cluster_data = data[data['cluster'] != -1]

    # Crear un DataFrame vacío para almacenar los datos limpios
    clean_data = pd.DataFrame(columns=['nombre_audio', 'cluster', 'categoria'])

    # Iterar sobre cada cluster único
    for cluster in cluster_data['cluster'].unique():
        # Obtener las filas correspondientes al cluster actual
        cluster_rows = cluster_data[cluster_data['cluster'] == cluster]

        # Calcular la categoría mayoritaria en el cluster
        mode_series = cluster_rows['categoria'].mode()

        if not mode_series.empty:
            majority_category = mode_series.iloc[0]
        else:
            majority_category = cluster_rows['categoria'].iloc[0]

        # Seleccionar una fila con la categoría mayoritaria
        selected_rows = cluster_rows[cluster_rows['categoria'] == majority_category]

        if not selected_rows.empty:
            selected_row = selected_rows.iloc[0]
        else:
            selected_row = cluster_rows.iloc[0]

        # Agregar la fila seleccionada al DataFrame limpio
        clean_data = clean_data.append(selected_row, ignore_index=True)

    # Exportar los archivos CSV
    clean_data.to_csv(output_clean_csv, index=False)
    noise_data.to_csv(output_noise_csv, index=False)


if __name__ == "__main__":
    # Cambia los nombres de archivo según sea necesario
    input_csv = "/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/CLUSTERING/resultado_clustering_gral_1_CLUSTER_X_NOMBRE_ARCH.csv"
    output_clean_csv = "/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/CLUSTERING/clustering_gral_1_SOLO_NOMBRE_ARCH.csv"
    output_noise_csv = "/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/CLUSTERING/clustering_gral_NOISE.csv"

    clean_dataset(input_csv, output_clean_csv, output_noise_csv)
