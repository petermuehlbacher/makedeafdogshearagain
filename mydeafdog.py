# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:17:03 2016

@author: YaY
"""
from scipy import *
from pylab import *

import wave
import struct
import subprocess
    
    

def sampleToSound(sample, framerate = 44100, name = 'sample.wav'):
    
    string = 'rm ' + name
    subprocess.call(string, shell=True)
    
    
    cp = wave.open( name , 'w')
    
    cp.setparams((1, 2, framerate, 0, 'NONE', 'not compressed'))
    
    values = []
    
    for k in range(len(sample)):                    
        value = int(sample[k])                      
        packed_value = struct.pack('h', value)      
        values.append(packed_value)
        
    value_str = bytes().join(values)
    cp.writeframes(value_str)
                
        
    cp.close()
    
    

def soundToSample(filename):
    wf = wave.open(filename,'r')
    
    channel = wf.getnchannels()
    framerate = wf.getframerate()
    
    samples = []
    tmp = wf.readframes(1)

    if channel == 1:
        while tmp != '' :                           # wird wf.getnframes() mal durchlaufen 
            data = struct.unpack('h', tmp)
            samples.append(int(data[0]))
            tmp = wf.readframes(1)
            
    else:
        while tmp != '' :                       
            data = struct.unpack('hh', tmp)
            samples.append(int((data[0]+data[1])/2)) # bei Stereo werden linker und rechter Sound gemittelt
            tmp = wf.readframes(1)
        
    wf.close()
    
    return samples, framerate
    
    
      
    
def pixelToIndex(x,y, resolution):
    """Returns the index int 0<=index<l^2; this is a bijective mapping
    from $l\times l\subset\mathbb R^2$ to $l^2\subset\mathbb R$,
    given by the (resolution)-th iteration of the Peano curve family"""
    
    index = ''

    indexMatrix = np.arange(4).reshape((2, 2))

    
    for i in range(resolution):

        currX = (x>>(resolution-i-1))%2
        currY = (y>>(resolution-i-1))%2
        
        quadrant = indexMatrix[currX][currY]
        
        index += '{0:02b}'.format(quadrant)
        
        if quadrant == 0:
            indexMatrix = np.transpose(indexMatrix)
        
        if quadrant == 3:
            indexMatrix = np.fliplr(np.transpose(np.fliplr(indexMatrix)))
    
    return int(index,2)