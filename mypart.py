# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 20:06:51 2016

@author: YaY
"""
from scipy import *
from pylab import *
import scipy.misc as sm

freq = sm.imread('small.png', True)
l = size(freq)
result = sm.toimage(freq)

curve = list(range(size(freq)))



def freqToSample(freq, sec, framerate = 44100):
    
    a,b = getCoeff(freq)
        
    sampleLength = sec * framerate    
    time = linspace(0,sec,sampleLength)
    
    samples = []
    
    for t in time:
        sum = 0
        for k in range(l//2+1):
            sum += a[k]*cos(k*t)+b[k]*sin(k*t)
            
        samples.append(sum)
        
    return samples
    


def getCoeff(freq):
        
        # FALLUNTERSCHEIDUNG FEHLT !!!
        
    l = size(freq)
    
    a = zeros(l//2+1)
    b = zeros(l//2+1)
    
    for k in range(l//2):
        b[-(k+1)] = curve[k]
        a[k] = curve[k+l//2]
        
    return a,b
    

    
    
    