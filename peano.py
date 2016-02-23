# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:23:13 2016

@author: YaY
"""
from scipy import *
from pylab import *
from mydeafdog import *

resolution=3
l=2**resolution

XYtoIndex = [None]*l
indexToX  = [None]*(l**2)
indexToY  = [None]*(l**2)

for x in range(l):
    XYtoIndex[x] = [None]*l
    for y in range(l):
        i = pixelToIndex(x,y,resolution)
        XYtoIndex[x][y] = i
        indexToX[i] = x
        indexToY[i] = y