from netCDF4 import Dataset
from glob import glob

# Ruta de la carpeta con las bandas de imágenes
ruta_carpeta_bandas = "D:\\Fer\\ceniza_LANOT\\temporal\\*"

# Obtener una lista de nombres de archivos en la carpeta
nombres_archivos = glob(ruta_carpeta_bandas)

for i in nombres_archivos:
    rootgrp = Dataset(i,"r", format="NETCDF4")
    
    print(rootgrp.dimensions)

rootgrp.close()