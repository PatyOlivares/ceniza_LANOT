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

                                

    