from netCDF4 import Dataset
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

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
#-------------------------------------------------------------------------------------------------#
# Tamaño del vecindario
vecindario_size = 5
min_good = 3

def calculate_neighborhood_operation(matrix, row, col, size):
    half_size = size // 2
    start_row = max(row - half_size, 0)
    end_row = min(row + half_size + 1, matrix.shape[0])
    start_col = max(col - half_size, 0)
    end_col = min(col + half_size + 1, matrix.shape[1])
    
    neighborhood = matrix[start_row:end_row, start_col:end_col]
    
    # Verificar si hay suficientes píxeles en el vecindario (min_good)
    if neighborhood.size >= min_good:
        return np.mean(neighborhood)
    else:
        return np.nan  # O cualquier otro valor que quieras asignar cuando no hay suficientes píxeles

# Aplicar el cálculo de vecindario a la matriz y1_exprs
resultado_final = np.zeros_like(y1_exprs, dtype=np.float32)

for row in range(y1_exprs.shape[0]):
    for col in range(y1_exprs.shape[1]):
        resultado_final[row, col] = calculate_neighborhood_operation(y1_exprs, row, col, vecindario_size)

# Mostrar la imagen del resultado final con el cálculo de vecindario
plt.imshow(resultado_final)
plt.title("Resultado con cálculo de vecindario")
plt.show()
