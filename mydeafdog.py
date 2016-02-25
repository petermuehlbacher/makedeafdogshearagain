# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:17:03 2016

@author: YaY
"""
from scipy import *
from pylab import *
from cmath import atanh

import wave
import struct
import subprocess



def rescaling( x, c = 0.99, D = [-2**15,2**15-1], W = [0,255] ):

    w = W[1]-W[0]                           # lengthe of range
    d = D[1]-D[0]                           # length of domain

    T = 2 * atanh(2*c/w-1)                  # upper bound where 100*c % of the limit can theoretically be achieved
    t = [(k-D[0])/d * 2*T - T for k in x]             # rescaling the domain, so it matches to [-T,T]

    y = [((exp(k)/(1+exp(k))) * w + W[0])/c for k in t]

    return y


def freqToCoeff(freq):                                  # muss noch normiert werden !!!

    n = len(freq)
    coeff = zeros(n)

    for k in range(1,(n//2)):
        coeff[n//2-k] = real(1j*(freq[k]-freq[-k]))
        coeff[n//2+k] = real(freq[k]+freq[-k])
    coeff[n//2] = real(freq[0])
    coeff[0] = real(freq[-(n//2)])

    return coeff




def coeffToPixel(coeff):
    n = len(coeff)

    pixel = [k/(n*(2.**8))+128 for k in coeff]

    return pixel




def pixelToImage(pixel):
    n = size(pixel)
    l = int(sqrt(n))
    M = zeros([l,l])
    resolution = int(log2(l))

    indexToX  = [None for i in xrange(l**2)]
    indexToY  = [None for i in xrange(l**2)]

    for x in xrange(l):
        for y in xrange(l):
            i = pixelToIndex(x,y,resolution)
            indexToX[i] = x
            indexToY[i] = y


    for i in xrange(n):
        M[[l-indexToY[i]-1],indexToX[i]] = pixel[i]

    return M


def freqToImage(freq):

    coeff = freqToCoeff(freq)
    pixel = coeffToPixel(coeff)
    image = pixelToImage(pixel)

    return image






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




def pixelToIndex(x,y,resolution):
    """Returns the index int 0<=index<l^2; this is a bijective mapping
    from $l\times l\subset\mathbb R^2$ to $l^2\subset\mathbb R$,
    given by the (resolution)-th iteration of the Peano curve family"""

    index = ''

    indexMatrix = np.arange(4).reshape((2, 2))
    # initializing it within the function on purpose
    # so it gets reset every time the function is called
    indexMatrix[1] = indexMatrix[1][::-1] # swap the third and fourth node

    for i in range(resolution):
        # bitwise shift to the right so that the i-th bit is the first one from the left
        # then take mod 2 to eliminate all other bits that are to its left
        # this way we get the i-th (from the left) element of the numbers binary representation,
        # e.g. 2 = 000010 -> 1 for i=4
        currX = (x>>(resolution-i-1))%2
        currY = (y>>(resolution-i-1))%2

        # depending on what the parent is (the first and the fourth quadrant undergo some flipping)
        # this represents the information how many steps it is from the beginning of the current
        # square we are in; e.g. on the most coarse grained scale the left bottom is 0, left top 1,
        # right top 2 and right bottom 3; if the 'parent' was (e.g.) an element at the right bottom,
        # then everything is flipped, i.e. the left bottom is 2, the left top 1, the right top 0 and
        # the right bottom 3
        quadrant = indexMatrix[currX][currY]

        # append 00,01,10 or 11 depending on whether quadrant is 0,1,2 or 3 respectively
        index += '{0:02b}'.format(quadrant)

        # bottom left -> flip along y=x, with the first and third quadrant being invariant
        if quadrant == 0:
            indexMatrix = np.transpose(indexMatrix)
        # bottom right -> flip along y=-x, with the second and fourth quadrant being invariant
        if quadrant == 3:
            indexMatrix = np.fliplr(np.transpose(np.fliplr(indexMatrix)))

    return int(index,2)



def soundToImage(filename, resolution = 6):
    sample, framerate = soundToSample(filename)
    # resolution=6 yields chunks of ~1/10 seconds length with the framerate of 44100

    if framerate != 44100:
        print('wrong framerate!')
        return 0

    N = (2**resolution)**2

    chunk_num = len(sample) // N

    chunks = [sample[i*N:(i+1)*N] for i in range(chunk_num)]

    video = []

    for chunk in chunks:
        video.append(freqToImage(fft(chunk)))

    return video
