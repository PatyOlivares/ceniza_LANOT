import pandas as pd
import re
import os
import shutil

# Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = r"D:/Fer/ceniza_LANOT/input"

# Obtener una lista de nombres de archivos en la carpeta
nombres_archivos = os.listdir(ruta_carpeta_bandas)

#Filtro para identificar las fechas de inicio (s) por formato yyyymmddhhmmss 
patron_nombre = re.compile(r'_s(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})_')

#Segundo Filtro para identificar las bandas que se van a usar "4, 7, 11, 13, 14, 15"
patron_bandas= ["CMIPC-M3C04", "CMIPC-M3C07", "CMIPC-M3C11", "CMIPC-M3C13", "CMIPC-M3C14", "CMIPC-M3C15"]

#Una lista vacia para almacenar tuplas con el nombre de los archivos
archivos_filtrados = []

#Aplicamos el primer filtrado por nombre y luego por fecha
for nombre in nombres_archivos:
    match_fecha = patron_nombre.search(nombre)
    if match_fecha:
        fecha = ''.join(match_fecha.groups())
        
        #Se aplica el segundo patron para filtrar las bandas necesarias
        if any(banda in nombre for banda in patron_bandas):
            archivos_filtrados.append((nombre, fecha))
        
#PANDA TIME 
df = pd.DataFrame(archivos_filtrados, columns=['Nombre','Fecha'])

df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', format='%Y%m%d%H%M%S%f')

# Obtener la fecha más reciente
fecha_mas_reciente = df['Fecha'].max()

# Filtrar el DataFrame para obtener solo las filas con la fecha más reciente
archivos_mas_recientes = df[df['Fecha'] == fecha_mas_reciente]

# Crear una carpeta temporal para copiar las bandas más recientes
ruta_carpeta_temporal = r"D:/Fer/ceniza_LANOT/temporal"
os.makedirs(ruta_carpeta_temporal, exist_ok=True)

#Con un for copiar y pegar los archivos_mas_recientes a carpeta temporal
for i, fila in archivos_mas_recientes.iterrows():
  nombre_archivo = fila['Nombre']
  ruta_origen_archivo = os.path.join(ruta_carpeta_bandas, nombre_archivo)
  ruta_destino_archivo = os.path.join(ruta_carpeta_temporal, nombre_archivo)
  
  shutil.copy(ruta_origen_archivo, ruta_destino_archivo)
  