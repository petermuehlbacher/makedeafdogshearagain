# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 20:16:07 2016

@author: YaY
"""
from scipy import *
from pylab import *




def freqToCoeff(freq):
    
    n = len(freq)
    coeff = zeros(n)
    
    for k in range(1,(n//2)):
        coeff[n//2-k] = float(1j*(freq[k]-freq[-k]))
        coeff[n//2+k] = float(freq[k]+freq[-k])
    coeff[n//2] = float(freq[0])
    coeff[0] = float(freq[-(n//2)])
    
    return coeff


# Rechenzeit mit N = 100m n = 1000  ca. 3 min


N = 20               # Anzahl der verschiedenen Groessen
n = 200              # Anzahl der Durchlaeufe pro Groesse

y = [k*(2**15) for k in range(2,2*(N+2),2)]  # Obere Schranke; k ist die Dimenstion des Raumes / Anzahl der Samples in einem Signal

maxima = zeros(N)
test = zeros(n)

for k in range(0,N):    
    for l in range(n):
        samples = [(m-0.5)*(2**16) for m in rand(2*(k+2))]   # generiert ein Signal der Groesse 2*(k+2)
        test[l] = max(freqToCoeff(fft(samples)))
    
    maxima[k] = max(test)
    
    
plot(maxima,label='Testversuch')
plot(y, label='obere Schranke')
yscale('log')
legend(bbox_to_anchor=(1, 0.25))
