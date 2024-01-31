from netCDF4 import Dataset
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter

#Calculo de ceniza
#Variable a usar

#Resultados del algebra
x1 = y1_exprs
x2 = y2_exprs
x3 = y3_exprs
#x4 = #Nhood#
#x5 = banda 4#
#x6 = banda 14#
#x7 = banda 15#
#x8 = sol cenit 15 #
#x9 = phase#

A1 = if (x1 < 0 and x2 > 0 and x3 > 2) or x4 = 1:
    return 1
    elif:
    (x1 < 1 and x2 > -0.5 and x3 > 2) or x4 = 2: 
        return 2:
    else:
        return 0 
    
A2 = if (x1 < 0 and x2 > 0 and x3 > 2) or x4 = 1:
    return 1
    elif:
        (x1 < 1 and x2 > -0.5 and x3 > 2 and x5 >0.002 and x6 < 263) or x4 = 2:
            return 2
        else:
            return 0 
A3 = if (x1 < 0 and x2 > 0 and x3 > 2 and x5 > 0.002) or x4 = 1:
    return 1 
    elif:
        (x1 < 1 and x2 > -0.5 and x3 > 2 and x5 > 0.002) or x4 = 2:
            return 2 
        else: 
            return 0 
A4 = if (x8 > 85):
    return A1:
        else:
            x8 < 85 and x8 > 70:
                return A2:
                    else:
                        x8 < 70:
                            return A3:
                                else:
                                    return 0
A5 = if (A4 = 1):
    return A4:
        else:
            A4 = 2 and x2 >= -0.6:
                return 2
            else:
                A4 = 2 and x2 >= -1:
                    return 2:
                        elif: 
                            A4 = 2 and x2 >= -1.5:
                                return 3
                            else:
                                A4 = 2 and x2 < -1.5:
                                    return 0:
                                        else:
                                            return A4

A6 = if (A5 <= 2 and x3 <= 0):
    return 0:
        elif:
            A5 >= 3 and x3 <= 1.5:
                return 0:
                    else:
                        return A5

A7 = if (A6 = 2 and x9 = 1):
    return 4:
        elif:
            A6 = 2 and x9 = 4:
                return 0:
                    elif:
                        A6 = 3 and x9 =1:
                            return 5:
                                else:
                                    A6 = 3 and x9 >= 2:
                                        return 0 :
                                            else:
                                                return A6

                                

    import numpy as np

# Suponiendo que x1, x2, x3, x4, x5, x6, x8 y x9 son matrices NumPy de tamaño 1500x2500
x1 = np.random.random((1500, 2500))
x2 = np.random.random((1500, 2500))
x3 = np.random.random((1500, 2500))
x4 = np.random.randint(0, 3, size=(1500, 2500))
x5 = np.random.random((1500, 2500))
x6 = np.random.random((1500, 2500))
x8 = np.random.random((1500, 2500)) * 100  # Supongo que x8 es un valor en el rango 0-100
x9 = np.random.randint(1, 5, size=(1500, 2500))  # Supongo que x9 es un valor en el rango 1-4

# Expresiones condicionales equivalentes en Python

y1_expr = np.where((x1 < 0) & (x2 > 0) & (x3 > 2) | (x4 == 1), 1, np.where((x1 < 1) & (x2 > -0.5) & (x3 > 2) | (x4 == 2), 2, 0))

y2_expr = np.where((x1 < 0) & (x2 > 0) & (x3 > 2) | (x4 == 1), 1,
                   np.where((x1 < 1) & (x2 > -0.5) & (x3 > 2) & (x5 > 0.002) & (x6 < 273) | (x4 == 2), 2, 0))

y3_expr = np.where((x1 < 0) & (x2 > 0) & (x3 > 2) & (x5 > 0.002) | (x4 == 1), 1,
                   np.where((x1 < 1) & (x2 > -0.5) & (x3 > 2) & (x5 > 0.002) | (x4 == 2), 2, 0))

y4_expr = np.where(x8 > 85, y1_expr,
                   np.where((x8 < 85) & (x8 > 70), y2_expr,
                            np.where(x8 < 70, y3_expr, 0)))

y5_expr = np.where(y4_expr == 1, y4_expr,
                   np.where((y4_expr == 2) & (x2 >= -0.6), 2,
                            np.where((y4_expr == 2) & (x2 >= -1), 2,
                                     np.where((y4_expr == 2) & (x2 >= -1.5), 3,
                                              np.where((y4_expr == 2) & (x2 < -1.5), 0, y4_expr)))))

y6_expr = np.where((y5_expr <= 2) & (x3 <= 0), 0,
                   np.where((y5_expr >= 3) & (x3 <= 1.5), 0, y5_expr))

y7_expr = np.where((y6_expr == 2) & (x9 == 1), 4,
                   np.where((y6_expr == 2) & (x9 == 4), 0,
                            np.where((y6_expr == 3) & (x9 == 1), 5,
                                     np.where((y6_expr == 3) & (x9 >= 2), 0, y6_expr))))

# Puedes utilizar las variables y1_expr, y2_expr, y3_expr, y4_expr, y5_expr, y6_expr y y7_expr según tus necesidades.

print("y1_expr:")
print(y1_expr)

print("\ny2_expr:")
print(y2_expr)

print("\ny3_expr:")
print(y3_expr)

print("\ny4_expr:")
print(y4_expr)

print("\ny5_expr:")
print(y5_expr)

print("\ny6_expr:")
print(y6_expr)

print("\ny7_expr:")
print(y7_expr)
