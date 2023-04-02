import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_clusters(csv_path):
    # Leer el archivo CSV
    data = pd.read_csv(csv_path)

    # Crear un gráfico de barras con la cantidad de audios en cada cluster
    plt.figure(figsize=(15, 6))
    sns.countplot(data=data, x='cluster', palette='viridis')

    # Configurar las etiquetas y el título del gráfico
    plt.xlabel('Cluster')
    plt.ylabel('Cantidad de audios')
    plt.title('Distribución de audios por cluster')

    # Mostrar el gráfico
    plt.show()

if __name__ == "__main__":
    # Cambia 'result.csv' por el nombre de tu archivo CSV resultante
    csv_path = r"/media/nofi-ai/NOFI_2022/DESARROLLO/ESA/DATA/CLUSTERING/resultado_clustering.csv"
    visualize_clusters(csv_path)
