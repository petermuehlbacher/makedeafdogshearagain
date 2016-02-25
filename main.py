# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 20:16:07 2016

@author: YaY
"""
from scipy import *
from pylab import *
from mydeafdog import *
import os

import scipy.misc as sm
<<<<<<< HEAD
        
resolution = 5
filename = 'duck.wav'
name = filename[:-4]
os.system('mkdir '+ name)

video = soundToImage(filename,resolution)
=======


video = soundToImage('whistle.wav',5)
>>>>>>> origin/master

for k in range(len(video)):

    number = '{:05}'.format(k+1)
<<<<<<< HEAD
    string = name + '/'+ name + number + '.png'
    
    M = sm.toimage(video[k],video[k].max(),video[k].min())
    sm.imsave(string,M)

fps = 44100/(2**resolution)**2
makemovie = 'ffmpeg -f image2 -r {1} -i {0}/{0}%05d.png -vcodec mpeg4 -y {0}/{0}.mp4'.format(name,fps)

os.system(makemovie)
=======
    string = 'video/image' + number + '.png'

    M = sm.toimage(video[k],video[k].max(),video[k].min())
    sm.imsave(string,M)
>>>>>>> origin/master
