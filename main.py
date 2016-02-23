# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 20:16:07 2016

@author: YaY
"""
from scipy import *
from pylab import *
from mydeafdog import *

import scipy.misc as sm
        
        
video = soundToImage('duck.wav',5)

for k in range(len(video)):
    
    number = '{:05}'.format(k+1)
    string = 'video/image' + number + '.png'
    
    M = sm.toimage(video[k],video[k].max(),video[k].min())
    sm.imsave(string,M)
    