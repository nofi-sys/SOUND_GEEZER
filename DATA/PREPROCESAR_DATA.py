import re
import sqlite3
import pandas as pd


def categorizar(nombre_track):

    # Expresión regular para detectar "CAM"
    ss_pattern = r'CAM|REF'
    if re.search(ss_pattern, nombre_track):
        return 'CAM'

    # Expresión regular para detectar "AMB"
    amb_pattern = r'AMB|AMBMONO06|AMB-ST|AMBMONO05|AX'
    if re.search(amb_pattern, nombre_track):
      return 'AMB'

    # Expresión regular para detectar "DLG"
    dlg_pattern = r'DUB|DIALOG|DX|DIR|OFF|VOZ|OMF|CASTERMAN|DIR.dup1.07|LLAMADA|MADRE.dup1|COCO|DX2.8|DIR.dup1.08|DIR.06|ENTREVISTA|MADRE|DIRBACK|DIR.02|LANIÑA.dup1|DIRECTOS|DIR.05|DIR.07|DIR.dup1.04|MADREBIS.dup1|LA301bis.dup1|Yasser'
    if re.search(dlg_pattern, nombre_track):
      return 'DLG'

    # Expresión regular para detectar "MUS"
    mus_pattern = r'MUS|SONG|MUSICA|MÚSICA|MX|A11.MUSICA|LASSA|12.MUSICA|CANCION|TIMBAL_1'
    if re.search(mus_pattern, nombre_track):
      return 'MUS'

    # Expresión regular para detectar "S-S"
    ss_pattern = r'SFX|S-S|SONO|SS|PSS|PASOS|MONOSONO3|MONOSONO|FX|ss|MONOSONO5|VIENTOS|MONOSONO6'
    if re.search(ss_pattern, nombre_track):
      return 'S-S'

  # Si no se detecta ninguna de las categorías anteriores, devolver "XXX"
    return 'XXX'

# Conexión a la base de datos
conn = sqlite3.connect('ptfiles.db')

# Consulta para obtener los datos de la tabla REGIONES
query = '''
SELECT nombre_audio, nombre_track
FROM REGION
'''

# Ejecutar la consulta y cargar los resultados en un DataFrame de Pandas
df = pd.read_sql_query(query, conn)

# Cerrar la conexión a la base de datos
conn.close()

# Crear una nueva columna "categoria" y asignar etiquetas de categoría a cada fila
df['categoria'] = df['nombre_track'].apply(categorizar)

# Guardar el DataFrame en un archivo .csv
df.to_csv('audios_y_categoria_track.csv', index=False)


