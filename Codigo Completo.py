import pandas as pd
import re
import os
import shutil
from netCDF4 import Dataset
import netCDF4 as nc
import pvlib
from datetime import datetime, timedelta
import numpy as np

# Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = r"D:\Fer\ceniza_LANOT\input"
# Ruta de la carpeta temporal
ruta_carpeta_temporal = r"D:\Fer\ceniza_LANOT\temporal"

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

## PARTE DE SOL CENIT #####-------------------------------------------------------------------------------------

# Define el patrón para la banda 15
patron_15 = "M3C15"

# Filtro para identificar las fechas de inicio (s) por formato sYYYYYDDDHHMMSSs
patron_nombre = re.compile(r'_s(\d{14})')

# Buscar archivos NetCDF en la carpeta
for archivo in os.listdir(ruta_carpeta_temporal):
    if patron_15 in archivo:
        # Buscar la fecha en el nombre del archivo
        match_fecha = patron_nombre.search(archivo)
        if match_fecha:
            # Obtener la fecha en formato juliano
            fecha_juliana = match_fecha.group(1)

            # Convertir la fecha juliana a formato estándar
            año = int(fecha_juliana[0:4])
            dia_del_año = int(fecha_juliana[4:7])
            hora = int(fecha_juliana[7:9])
            minuto = int(fecha_juliana[9:11])
            segundo = int(fecha_juliana[11:13])

            fecha_obj = datetime(año, 1, 1) + timedelta(days=dia_del_año - 1, hours=hora, minutes=minuto, seconds=segundo)

            # Imprimir resultados
            print(f"Encontré un archivo con M3C15: {archivo}")
            print(f"Fecha del archivo (juliana): {fecha_juliana}")
            print(f"Fecha convertida: {fecha_obj.strftime('%Y-%m-%d %H:%M:%S')}")

            # Abrir el archivo NetCDF y obtener la lista de variables
            ruta_nc = os.path.join(ruta_carpeta_temporal, archivo)
            with nc.Dataset(ruta_nc, 'r') as dataset:
                # Obtener la coordenada de subpunto nominal del satélite
                lat_satellite = dataset.variables['nominal_satellite_subpoint_lat'][0]
                lon_satellite = dataset.variables['nominal_satellite_subpoint_lon'][0]

                # Calcular la posición del sol en la escena usando pvlib
                solar_position = pvlib.solarposition.get_solarposition(
                    time=fecha_obj,
                    latitude=lat_satellite,
                    longitude=lon_satellite
                )

                # Obtener el ángulo cenital del sol
                sun_zenith = solar_position['zenith'].values[0]

                print(f"Sun Zenith: {sun_zenith:.2f} degrees")
            print("\n", "\n \n\n\n ---------------------------------------------------------")


#------------------------------------PARTE DE PATY - CREACION DICCIONARIO#-------------------------------------------------------#

#Obtener una lista de nombres de archivos en la carpeta SOLO LAS BANDAS
archivos_nc = [archivo_b for archivo_b in os.listdir(ruta_carpeta_temporal) if archivo_b.endswith('.nc') and 'ACTP' not in archivo_b]

variables = {}
#Leer los datos de los archios .nc

for archivo_b in archivos_nc:
    ruta_completa = os.path.join(ruta_carpeta_bandas, archivo_b)
    with Dataset(ruta_completa, 'r') as nc_file:
      CMI_values = nc_file.variables['CMI'][:]
 # Almacena las variables en el diccionario
    variables[archivo_b]= {'CMI':CMI_values}

#--------------#Transmisividad#--------------------------------------------------------------------------------------#
def trans(variables):
    
    # Obtener las claves ordenadas (siempre en el orden de bandas menor a mayor)
    ordered_keys = sorted(variables.keys())
    
    # Obtener las matrices 'CMI' de todas las bandas
    band_matrices = [variables[key]['CMI'].data for key in ordered_keys]
    
    # Definiendo variables
    # Cambiar el índice de 1 a 0, ya que las listas en Python comienzan desde 0
    x0 = band_matrices[0]  # banda 4
    x1 = band_matrices[1]  # banda 7
    x2 = band_matrices[2]  # banda 11
    x3 = band_matrices[3]  # banda 13
    x4 = band_matrices[4]  # banda 14
    x5 = band_matrices[5]  # banda 15

    # Banda 13 - Banda 15
    y1_expr = x3 - x5
    # Banda 11 - Banda 13
    y2_expr = x2 - x3
    # Banda 7 - Banda 13
    y3_expr = x1 - x3
    
    # Luego, puedes imprimir o hacer lo que necesites con los resultados
    return y1_expr, y2_expr, y3_expr, x0, x4, x5

# Llamar a la función trans y obtener los resultados
y1_expr, y2_expr, y3_expr, x0, x4, x5 = trans(variables)

#-----------------------------# NEIGHBORHOOD #------------------------------------#

def nhood(variables, box_sides=(5, 5), min_good=3):
    # Obtener las claves ordenadas (siempre en el orden de bandas menor a mayor)
    ordered_keys = sorted(variables.keys())
    
    # Obtener las matrices 'CMI' de todas las bandas
    band_matrices = [variables[key]['CMI'].data for key in ordered_keys]

    # Usar la matriz de la banda 13 como referencia para el cálculo del vecindario
    x1 = band_matrices[3]  # La banda 13 está en la posición 2 (índice 2) en band_matrices
    x2 = band_matrices[5] # CARGO LA BANDA 15 PERO NO SE POR QUE? 
    x3 = x1 - x2
    
    # Calcular el vecindario.
    vecindario = np.lib.stride_tricks.sliding_window_view(x1, box_sides)

    # Evaluar la expresión.
    resultado = np.where(np.logical_and(x3 < 0, x3 - (np.mean(vecindario) + np.std(vecindario)) < -1), 1,
                         np.where(np.logical_and(x3 < 1, x3 - (np.mean(vecindario) + np.std(vecindario)) < -1), 2, 0))

    return resultado

#Llamamos a la funcion neighbor y obtenemos el resultado
neighbor = nhood(variables)

#---------------------------------------LAS CONDICIONALES DE CENIZA----------------------------------------------------------#

#RENOMBRANDO Variables que ya tenemos
x1 = y1_expr
x2 = y2_expr
x3 = y3_expr
x4 = neighbor
x5 = x4
x6 = x4
x7 = x5
x8 = sun_zenith
#x9 = phase # <-------------- la phase está dentro de la mascará osea el archivo ACTP

CENIZA_N = np.zeros_like(x1, dtype=np.int8)
CENIZA_CREP = np.zeros_like(x1, dtype=np.int8)
CENIZA_D = np.zeros_like(x1, dtype=np.int8)


# Noche
CENIZA_N = np.where((x1 < 0) & (x2 > 0) & (x3 > 2) | (x4 == 1), 1, np.where((x1 < 1) & (x2 > -0.5) & (x3 > 2) | (x4 == 2), 2, 0))

# Crepusculo
CENIZA_CREP = np.where((x1 < 0) & (x2 > 0) & (x3 > 2) | (x4 == 1), 1,
                   np.where((x1 < 1) & (x2 > -0.5) & (x3 > 2) & (x5 > 0.002) & (x6 < 273) | (x4 == 2), 2, 0))

# Día 
CENIZA_D = np.where((x1 < 0) & (x2 > 0) & (x3 > 2) & (x5 > 0.002) | (x4 == 1), 1,
                   np.where((x1 < 1) & (x2 > -0.5) & (x3 > 2) & (x5 > 0.002) | (x4 == 2), 2, 0))

#FALTA POR COMPROBAR#

CENIZA_TIEMPO = np.where(x8 > 85, CENIZA_N,
                   np.where((x8 < 85) & (x8 > 70), CENIZA_CREP,
                            np.where(x8 < 70, CENIZA_D, 0)))

CENIZA_UM1 = np.where(CENIZA_TIEMPO == 1, CENIZA_TIEMPO,
                   np.where((CENIZA_TIEMPO == 2) & (x2 >= -0.6), 2,
                            np.where((CENIZA_TIEMPO == 2) & (x2 >= -1), 2,
                                     np.where((CENIZA_TIEMPO == 2) & (x2 >= -1.5), 3,
                                              np.where((CENIZA_TIEMPO == 2) & (x2 < -1.5), 0, CENIZA_TIEMPO)))))

CENIZA_UM2 = np.where((CENIZA_UM1 <= 2) & (x3 <= 0), 0,
                   np.where((CENIZA_UM1 >= 3) & (x3 <= 1.5), 0, CENIZA_UM1))

CENIZA = np.where((CENIZA_UM2 == 2) & (x9 == 1), 4,
                   np.where((CENIZA_UM2 == 2) & (x9 == 4), 0,
                            np.where((CENIZA_UM2 == 3) & (x9 == 1), 5,
                                     np.where((CENIZA_UM2 == 3) & (x9 >= 2), 0, CENIZA_UM2))))


