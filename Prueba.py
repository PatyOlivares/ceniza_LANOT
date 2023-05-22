#Función de nombres 
import os
import shutil
import tarfile
import numpy as np
import gdal


input_dir = "input"

#Para los procesos temporales y de salida 
temp_dir = "temp"
output_dir = "out"

#Lista de los archivos de entrada y búsqueda del último Canal (C16)
files = os.listdir(input_dir)
lastfile = os.path.join(input_dir, files[-1])
print(os.path.basename(lastfile))
lastfile
files

#Mover el archivo al directorio de trabajo  
shutil.move(lastfile, temp_dir)
os.chdir(temp_dir)

#Descomprimir 
descomp = gdal.Open(lastfile)

for filename in os.listdir('.'):
    if filename.endswith(.tif):
        tar = tarfile.open(filename)
        tar.extractall()
        tar.close()



#Para cortar el nombre 

#lastname = lastfile


#def cortarnom():
    ##aki va la función de los nombres 
    # #Definición de funciones
    
#def last (input): 
    #for blabla 
    #var = "last result" 

    #return var 