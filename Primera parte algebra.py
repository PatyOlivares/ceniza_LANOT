
from netCDF4 import Dataset
from glob import glob
import matplotlib.pyplot as plt
import numpy

# Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = "D:\\Fer\\ceniza_LANOT\\temporal\\*"

# Obtener una lista de nombres de archivos en la carpeta
nombres_archivos = glob(ruta_carpeta_bandas)

# Nombres de las bandas correspondientes
nombres_bandas = ["b4", "b7", "b11", "b13", "b14", "b15"]

# Diccionario para almacenar las bandas
bandas = {}

for nombre_archivo, nombre_banda in zip(nombres_archivos, nombres_bandas):
    with Dataset(nombre_archivo, 'r', format='NETCDF4') as nc_file:
        arreglo = nc_file['CMI'][:]
        bandas[nombre_banda] = arreglo
        plt.imshow(arreglo)
        plt.title(nombre_banda)
        plt.show()
#--------------------------------------------------------------------------------------------#
# se crean variables para realizar la resta de las bandas
b13 = bandas["b13"]
b15 = bandas["b15"]
b11= bandas["b11"]
b07= bandas["b7"]
y1_exprs = b13-b15
y2_exprs = b11-b13
y3_exprs = b07-b13
plt.imshow(y2_exprs)
#--------------------------------------------------------------------------------------------#


