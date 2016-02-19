# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:26:43 2016

@author: YaY
"""
from scipy import *
from pylab import *
import wave
import struct
import subprocess

filename = 'glass.wav'

s, f = soundToSample(filename)
sampleToSound(s,f)


def soundToSample(filename):
    wf = wave.open(filename,'r')
    
    channel = wf.getnchannels()
    framerate = wf.getframerate()
    
    sample = []
    tmp = wf.readframes(1)

    if channel == 1:
        while tmp != '' :                       # sollte wf.getnframes() mal durchlaufen werden
            data = struct.unpack('h', tmp)
            sample.append(int(data[0]))
            tmp = wf.readframes(1)
            
    else:
        while tmp != '' :                       
            data = struct.unpack('hh', tmp)
            sample.append(int((data[0]+data[1])/2)) # bei Stereo werden linker und rechter Sound gemittelt
            tmp = wf.readframes(1)
        
    wf.close()
    
    return sample, framerate
    


def sampleToSound(sample, framerate = 44100, name = 'copy.wav'):
    
    string = 'rm ' + name
    subprocess.call(string, shell=True)
    cp = wave.open( name , 'w')
    
    cp.setparams((1, 2, framerate, 0, 'NONE', 'not compressed'))
    
    for k in range(len(sample)):
        value = int(sample[k])
        packed_value = struct.pack('h', value)
        cp.writeframes(packed_value)
        
    cp.close()
    
