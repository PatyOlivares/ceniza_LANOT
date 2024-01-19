import os
import re
import netCDF4 as nc
import pvlib
from datetime import datetime, timedelta

# Ruta de la carpeta que contiene los archivos NetCDF
carpeta = r"D:\Fer\ceniza_LANOT\temporal"

# Define el patrón para la banda 15
patron_15 = "M3C15"

# Filtro para identificar las fechas de inicio (s) por formato sYYYYYDDDHHMMSSs
patron_nombre = re.compile(r'_s(\d{14})')

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

            # Abrir el archivo NetCDF y calcular el sol cenital
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
                sun_zenith = solar_position['zenith']

                # Imprimir el ángulo cenital del sol
                print(f"Sun Zenith: {sun_zenith.values[0]:.2f} degrees")

            print("\n")
