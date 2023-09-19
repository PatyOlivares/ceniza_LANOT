from netCDF4 import Dataset
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter

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

# Se crean variables para realizar la resta de las bandas
b13 = bandas["b13"]
b15 = bandas["b15"]
b11 = bandas["b11"]
b07 = bandas["b7"]
y1_exprs = b13 - b15
y2_exprs = b11 - b13
y3_exprs = b07 - b13
plt.imshow(y2_exprs)
# ... [resto del código anterior hasta la definición de y2_exprs] ...

plt.imshow(y2_exprs)

# Estadísticas de nhood_y1 antes de procesamiento:
print("Estadísticas de nhood_y1 antes de procesamiento:")
print("Media:", np.mean(y1_exprs))
print("Mediana:", np.median(y1_exprs))
print("Desviación estándar:", np.std(y1_exprs))
print()

# Función para la lógica de vecindad
def compute_value(x, avg, std_dev):
    if x < 0 and (x - avg + std_dev) < -1:
        return 1
    elif x < 1 and (x - avg + std_dev) < -1:
        return 2
    else:
        return 0

# Función para aplicar en cada ventana
def func_window(window):
    min_good_pixels = 3
    center_pixel = window[len(window) // 2]
    
    # Si hay píxeles faltantes en la ventana (es decir, NaNs o similar),
    # simplemente devuelve el pixel central
    if np.sum(np.isnan(window)) > (box_sides[0] * box_sides[1] - min_good_pixels):
        return center_pixel
    
    avg = np.mean(window)
    std_dev = np.std(window)
    
    return compute_value(center_pixel, avg, std_dev)

# Aplica la ventana deslizante de 5x5 a nhood_y1
box_sides = (5, 5)
nhood_y1_processed = generic_filter(y1_exprs, func_window, size=box_sides)

# ... [resto del código para visualización y análisis] ...

