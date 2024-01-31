import netCDF4 as nc

# Ruta del archivo NetCDF
ruta_nc = r"D:\Fer\ceniza_LANOT\temporal\CG_ABI-L2-ACTPC-M3_G16_s20190721557191_e20190721559575_c20190721600012.nc"

# Abrir el archivo NetCDF
with nc.Dataset(ruta_nc, 'r') as dataset:
    # Imprimir las claves disponibles en el conjunto de datos
    print(dataset.variables.keys())

#Para cada variable, imprimir sus dimensiones y atributos
for var_name, variable in dataset.variables.items():
    print(f"\nVariable: {var_name}")
    print("Dimensions:", variable.dimensions)
    print("Attributes:", variable.__dict__)



# Abrir el archivo NetCDF
with nc.Dataset(ruta_nc, 'r') as dataset:
    # Imprimir información sobre las variables 't' y 'time_bounds'
# Intentar acceder a los valores de la variable 't' usando otro método
    try:
        valores_t = dataset.variables['t'][:]
        print("Valores de t:", valores_t)
    except Exception as e:
            print("Error al acceder a t:", e)
            print("---------------------")
# Intentar acceder a los valores de la variable 'time_bounds' usando otro método
    try:
        valores_time_bounds = dataset.variables['time_bounds'][:]
        print("Valores de time_bounds:", valores_time_bounds)
    except Exception as e:
            print("Error al acceder a time_bounds:", e)