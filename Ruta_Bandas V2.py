import os
import re
from netCDF4 import Dataset

# Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = r"D:/Fer/ceniza_LANOT/input"

# Obtener una lista de nombres de archivos en la carpeta
nombres_archivos = os.listdir(ruta_carpeta_bandas)

# Patrón para extraer la fecha de los nombres de archivos
patron_fecha = r"_s(\d{14})_e(\d{14})_c(\d{14})\.nc"

# Lista para almacenar las fechas
fechas = []
# Lista con las bandas necesarias
bandas = ["CG_ABI-L2-CMIPC-M3C04_G16", "CG_ABI-L2-CMIPC-M3C07_G16", "CG_ABI-L2-CMIPC-M3C11_G16", 
          "CG_ABI-L2-CMIPC-M3C13_G16", "CG_ABI-L2-CMIPC-M3C14_G16", "CG_ABI-L2-CMIPC-M3C15_G16"]

# Iterar a través de los nombres de archivos y obtener las fechas
for nombre_archivo in nombres_archivos:
    fecha_match = re.search(patron_fecha, nombre_archivo)
    if fecha_match:
        fecha = fecha_match.group(1)
        fechas.append(fecha)

# Encontrar la fecha más reciente
fecha_mas_reciente = max(fechas)

# Patrón para verificar si un nombre de archivo contiene la fecha más reciente
patron_fecha = re.compile(r"_s" + fecha_mas_reciente)

# Lista para almacenar los nombres de archivos que coinciden con la fecha
archivos_con_fecha_reciente = []

# Iterar a través de los nombres de archivos y verificar la fecha
for nombre_archivo in nombres_archivos:
    if patron_fecha.search(nombre_archivo):
        archivos_con_fecha_reciente.append(nombre_archivo)

#Lista para almacenar los nombres de archivos filtrados por el patron
archivos_con_fecha_reciente_filtrados = []

#Iterar 2 listas y verificar el patron
for cadena in archivos_con_fecha_reciente:
    for patron in bandas:
        if re.search(patron, cadena):
            archivos_con_fecha_reciente_filtrados.append(cadena)

# Crear una carpeta temporal para copiar las bandas más recientes
ruta_carpeta_temporal = r"D:/Fer/ceniza_LANOT/temporal"
os.makedirs(ruta_carpeta_temporal, exist_ok=True)

# Copiar los archivos correspondientes a la carpeta temporal usando os.system
for nombre_archivo in archivos_con_fecha_reciente_filtrados:
    comando_copiar = f'copy "{os.path.join(ruta_carpeta_bandas, nombre_archivo)}" "{ruta_carpeta_temporal}"'
    resultado = os.system(comando_copiar)
    if resultado == 0:
        print(f"Se copió {nombre_archivo} a {ruta_carpeta_temporal}")
    else:
        print(f"No se pudo copiar {nombre_archivo} a {ruta_carpeta_temporal}")

# Imprimir la ruta de la carpeta temporal
print("Los archivos se han copiado a la siguiente carpeta temporal:")
print(ruta_carpeta_temporal)
    
# Imprimir la fecha más reciente
print("La fecha más reciente es:", fecha_mas_reciente)
