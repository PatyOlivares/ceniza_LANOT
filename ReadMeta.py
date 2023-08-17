#Importando biblioteca 
import rasterio

#creando función
def metadata(path_input):
    
    with rasterio.open(path_input) as src:
        datos = src.meta
        crs = src.crs
        dataset = src.read()
        metadata = src.meta
        height = src.height
        width = src.width
        transform = src.transform
        
# Fecha del título de la imagen
        title = path_input
        Fechas = title.split('-')[1].split('.')
        Año = Fechas[0]
        Mes = Fechas[1][0:2]
        Día = Fechas[1][2:4]
        
# Creando un diccionario con la información de la banda

        Dic_meta = {'dataset' : dataset, 'METADATO:': metadata, 'ALTURA:':height, 'ANCHO:':width, 
                    'TRANSFORMADA':transform, 'SISTM COORD:':crs, 'AÑO': Año, 'MES': Mes, 'DIA': Día}
        
# Utilizar la transformada para convertir datos de tamaño de pixel
        

# Aquí estoy regresando los valores que obtuve en (dentro de) la función, variable datos contiene el metadato, dic_meta es mi diccionario
    return datos, Dic_meta

# Debo encontrar una manera de leer las bandas que esten en la carpeta temporal

path_input = 'D:\Fer\ceniza_LANOT\input\goes16.abi-2023.0312.0850-CMI-C01_1km.tif'

# Aquí llamo a la función y guardo el diccionario resultante en 2 variables (preguntar a Uri si es necesario)
datos, diccionario = metadata(path_input)

# Imprimí el SOLO 'diccionario' para verificar que la información de la fecha se haya agregado correctamente
print("aqui está la informacion de imagen\n", diccionario)
