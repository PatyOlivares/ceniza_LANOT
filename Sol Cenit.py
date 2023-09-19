import rasterio
from datetime import datetime
import pvlib
import pytz

# Ruta al archivo de la imagen satelital GeoTIFF
file_path = 'D:\Fer\ceniza_LANOT\input\goes16.abi-2023.0312.0850-CMI-C15_2km.tif'

# Extrae la fecha y hora del nombre del archivo
file_name = file_path.split('/')[-1]  # Obtiene el nombre del archivo de la ruta
date_str = file_name.split('-')[1]  # Extrae la parte de la fecha y hora del nombre del archivo
time = datetime.strptime(date_str, '%Y.%m%d.%H%M')

# Abre la imagen raster con rasterio
with rasterio.open(file_path) as dataset:
    # Obtiene la información de la proyección
    crs = dataset.crs

    # Obtiene la latitud y longitud del centro de la imagen (proyección geos)
    lon, lat = dataset.xy(dataset.height // 2, dataset.width // 2, offset='center')

from datetime import datetime

# Coordenadas de la ubicación de observación
latitude = lat  # Latitud en grados
longitude = lon  # Longitud en grados

# Fecha y hora en la que se tomó la imagen
observation_time = datetime(2023, 8, 17, 8, 50, tzinfo=pytz.UTC)

# Calcula la posición solar
solar_position = pvlib.solarposition.get_solarposition(
    observation_time, latitude, longitude, method='nrel_numpy'
)

# Calcula el ángulo cenital solar (solar zenith angle)
solar_zenith_angle = 90 - solar_position['elevation']
    
# Imprime el ángulo cenital solar
print("Ángulo Cenital Solar:", solar_zenith_angle)


# Imprime los metadatos
print("Latitud:", lat)
print("Longitud:", lon)
print("Fecha y Hora:", time)
