import pandas as pd
import re
import os
import shutil
from netCDF4 import Dataset

# Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = r"D:/Fer/ceniza_LANOT/input"
# Ruta de la carpeta temporal
ruta_carpeta_temporal = r"D:/Fer/ceniza_LANOT/temporal"

# Limpiar la carpeta temporal si existe
if os.path.exists(ruta_carpeta_temporal):
    shutil.rmtree(ruta_carpeta_temporal)

# Crear una carpeta temporal
os.makedirs(ruta_carpeta_temporal)

# Obtener una lista de nombres de archivos en la carpeta
nombres_archivos = os.listdir(ruta_carpeta_bandas)

# Filtro para identificar las fechas de inicio (s) por formato yyyymmddhhmmss
patron_nombre = re.compile(r'_s(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})')

# Patrón para la máscara
patron_mascara = "ACTPC-M3_G16"

# Lista vacía para almacenar tuplas con el nombre de los archivos
archivos_bandas = []
archivos_mascara = []

# Aplicamos el primer filtrado por nombre y luego por fecha y máscara
for nombre in nombres_archivos:
    match_fecha = patron_nombre.search(nombre)
    if match_fecha:
        fecha = ''.join(match_fecha.groups())

        # Filtrar por bandas
        for banda in ["M3C04", "M3C07", "M3C11", "M3C13", "M3C14", "M3C15"]:
            if banda in nombre:
                archivos_bandas.append((nombre, fecha))
                break

        # Filtrar por máscara
        if patron_mascara in nombre:
            archivos_mascara.append((nombre, fecha))

# PANDA TIME para bandas
df_bandas = pd.DataFrame(archivos_bandas, columns=['Nombre', 'Fecha'])
df_bandas['Fecha'] = pd.to_datetime(df_bandas['Fecha'], errors='coerce', format='%Y%m%d%H%M%S%f')

# PANDA TIME para máscara
df_mascara = pd.DataFrame(archivos_mascara, columns=['Nombre', 'Fecha'])
df_mascara['Fecha'] = pd.to_datetime(df_mascara['Fecha'], errors='coerce', format='%Y%m%d%H%M%S%f')

# Redondear las fechas a segundos para ignorar microsegundos
df_bandas['Fecha'] = df_bandas['Fecha'].dt.round('1s')
df_mascara['Fecha'] = df_mascara['Fecha'].dt.round('1s')

# Obtener la fecha más reciente para bandas
fecha_mas_reciente_bandas = df_bandas['Fecha'].max()

# Filtrar el DataFrame para obtener solo las filas con la fecha más reciente para bandas
archivos_mas_recientes_bandas = df_bandas[df_bandas['Fecha'] == fecha_mas_reciente_bandas]

# Obtener la fecha más reciente para máscara
fecha_mas_reciente_mascara = df_mascara['Fecha'].max()

# Filtrar el DataFrame para obtener solo las filas con la fecha más reciente para máscara
archivos_mas_recientes_mascara = df_mascara[df_mascara['Fecha'] == fecha_mas_reciente_mascara]

# Combinar los resultados
archivos_mas_recientes = pd.concat([archivos_mas_recientes_bandas, archivos_mas_recientes_mascara])

# Con un for copiar y pegar los archivos_mas_recientes a carpeta temporal
for i, fila in archivos_mas_recientes.iterrows():
    nombre_archivo = fila['Nombre']
    ruta_origen_archivo = os.path.join(ruta_carpeta_bandas, nombre_archivo)
    ruta_destino_archivo = os.path.join(ruta_carpeta_temporal, nombre_archivo)

    shutil.copy(ruta_origen_archivo, ruta_destino_archivo)

#Obtener una lista de nombres de archivos en la carpeta SOLO LAS BANDAS
posicion = 11
letra = 'C'
archivos_nc = [archivo_b for archivo_b in os.listdir(ruta_carpeta_temporal) if archivo_b.endswith('.nc') and 'ACTP' not in archivo_b]

variables = {}
#Leer los datos de los archios .nc

for archivo_b in archivos_nc:
    ruta_completa = os.path.join(ruta_carpeta_bandas, archivo_b)
    with Dataset(ruta_completa, 'r') as nc_file:
      CMI_values = nc_file.variables['CMI'][:]
 # Almacena las variables en el diccionario
    variables[archivo_b]= {'CMI':CMI_values}
    
