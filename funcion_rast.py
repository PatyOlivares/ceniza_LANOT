# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 13:03:30 2023

@author: LANOT_01
"""

#importamos rasterio
import rasterio
ruta = "./input/goes16.abi-2023.0312.0850-CMI-C01_1km.tif"
#obteniendo contexto del bloque para abrir la ruta con rasterio 
with rasterio.open(ruta) as rast:
     print(type(rast))


    