
import os
import re
import netCDF4 as nc
import pvlib
from datetime import datetime, timedelta
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
# Ruta de la carpeta que contiene los archivos NetCDF
carpeta = r"E:\PATY_2023\ceniza_LANOT\temporal"

# Define el patrón para la banda 15
patron_15 = "M3C15"

# Filtro para identificar las fechas de inicio (s) por formato sYYYYYDDDHHMMSSs
patron_nombre = re.compile(r'_s(\d{14})')

# Diccionario para almacenar las correcciones
ch15 = {}

# Buscar archivos NetCDF en la carpeta
for archivo in os.listdir(carpeta):
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
            ruta_nc = os.path.join(carpeta, archivo)
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

                # Obtener los valores de píxeles de la banda 15
                banda15 = dataset.variables['CMI'][:]  # Ajustar según la lista de variables

                # Aplicar la corrección cosenoidal
                cos_sun_zenith = np.cos(np.radians(sun_zenith))
                banda15_corr = banda15 / cos_sun_zenith

                # Almacenar las correcciones en el diccionario
                ch15[archivo] = banda15_corr

                # Imprimir el ángulo cenital del sol
                print(f"Sun Zenith: {sun_zenith:.2f} degrees")

            print("\n", ch15, "\n \n\n\n ---------------------------------------------------------")
 #PARTE DE LA TRANSIMIIDAD
 # Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = 'E:\\PATY_2023\\ceniza_LANOT\\temporal'

# Obtener una lista de nombres de archivos en la carpeta
archivos_nc = [archivo_b for archivo_b in os.listdir(ruta_carpeta_bandas) if archivo_b.endswith('.nc')]

variables = {}
#Leer los datos de los archios .nc

for archivo_b in archivos_nc:
    ruta_completa = os.path.join(ruta_carpeta_bandas, archivo_b)
    with Dataset(ruta_completa, 'r') as nc_file:
       CMI_values = nc_file.variables['CMI'][:]
 # Almacena las variables en el diccionario
       variables[archivo_b]= {'CMI':CMI_values}
     
if len(variables) >= 6:
    y1_expr = variables[archivos_nc[3]]['CMI'] - ch15[archivo]
    y2_expr = variables[archivos_nc[2]]['CMI'] - variables[archivos_nc[3]]['CMI']
    y3_expr = variables[archivos_nc[1]]['CMI'] - variables[archivos_nc[3]]['CMI']
#RECTIFICACION
    #print("\nCalculando transimividad Inversa\n")
   # print("Resultado y1:", y1_expr)
   # print("Resultado y2:", y2_expr)
   # print("Resultado y3:", y3_expr)
   # plt.imshow(y1_expr)

             
  
#pats=11=
 # re.compile(r'M3C04',re.IGNORECASE),re.compile(r'M3C07',re.IGNORECASE),re.compile(r'M3C11',re.IGNORECASE)]
#bandas_alg={}
#for i in  variables[archivo_b]:
   # for pattern in pats:
        #res=re.search(pattern,i)
       # if res !=None:
           # bandas_alg[pattern.pattern]=variables[archivo_b]

            
# Imprimir un ejemplo de la matriz de valores de píxeles de la Banda 15 ajustada
#if ch15:
   # ejemplo_archivo = next(iter(ch15.keys()))  # Tomar el primer archivo en ch15
   # valores_pixel_ajustados = ch15[ejemplo_archivo]
    #print(f"Ejemplo de valores de píxeles ajustados para {ejemplo_archivo}:\n{valores_pixel_ajustados}")
#else:
    #print("El diccionario ch15 está vacío.")
#PARA QUIEN LEA,a2Qghc ES EL DICCIONARIO QUE CONTIENE LOS VALORES DE PIXEL AJUSTADOS C