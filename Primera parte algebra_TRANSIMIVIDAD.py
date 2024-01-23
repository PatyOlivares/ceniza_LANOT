
import os
from netCDF4 import Dataset
from glob import glob
import matplotlib.pyplot as plt
import numpy

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

if len(variables.keys()) >= 6:
    y1_expr = variables[archivos_nc[3]]['CMI'] - ch15[archivo]
    y2_expr = variables[archivos_nc[2]]['CMI'] - variables[archivos_nc[3]]['CMI']
    y3_expr = variables[archivos_nc[1]]['CMI'] - variables[archivos_nc[3]]['CMI']
#RECTIFICACION
    print("\nCalculando transimividad Inversa\n")
    print("Resultado y1:", y1_expr)
    print("Resultado y2:", y2_expr)
    plt.imshow(y1_expr)