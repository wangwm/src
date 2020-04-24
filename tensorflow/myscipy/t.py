#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import math
import  traceback

import mylib as myScipy

my = myScipy.my_scipy()


x = np.array([1,2,3,4,5,6,7,8])     #x是一维数组 
d = x.reshape((2,4))                #将x重塑为2行4列的二维数组
y = 2*x

z = np.array([1.0,2.0,4.0,6.0,8.0,10.0])     #x是一维数组 
#z = np.array([1,2,600,800,10])     #x是一维数组 

print  my.linear_line(z)
print  my.linear_line2(z)
