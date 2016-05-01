"""
Filename: mainDistortion.py

See README.md

Developed under the Apache License 2.0
"""
#______________________________________________________________________________
#Header Imports
import array
import contextlib
import wave
import matplotlib.pyplot as plt
import numpy as np
import math
import copy 
import sys

sys.path.append('../Utilities')
import utilities as ut


#______________________________________________________________________________
#Start mainDistortion.py

# Global parameters
dirIn = "../../Original-Audio-Samples/"
dirOut = "../../Output-Audio-Samples/Distortion/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
maxAmp = (2**(8*sampleWidth - 1) - 1)    #maximum amplitude is 2**15 - 1  = 32767
minAmp = -(2**(8*sampleWidth - 1))       #min amp is -2**15


#______________________________________________________________________________


def distortion(signal, clipThreshold = .3, attack = .9):
 
    length = len(signal)
    increment = 1.1
    
    #increase gain to induce clipping
    while ut.signalCapPercent(signal) < clipThreshold:
        for i in range(length):
            signal[i] *= increment
    
    avg = ut.signalAvg(signal)
    overClippingPairs = [] 
    underClippingPairs = []
    
    #mark start and ending positions of clipping
    for i in range(length):
        if signal[i] > maxAmp:
            k = i
            while signal[k] > maxAmp:
                k += 1            
            if k != i:
                overClippingPairs += [[i,k]]
            
        elif signal[i] < minAmp:
            j = i
            while signal[k] > maxAmp:
                j += 1            
            if j != i:
                underClippingPairs += [[i,j]]
    
    for pair in overClippingPairs:
        start = pair[0]
        end = pair[1]
        eventLength = end-start
        middle = []
        if (eventLength)%2==1:
            middle += [ start + ((eventLength // 2) + 1) ]        
            
        else:
            middle += [start + (eventLength // 2)]
            middle += [start + ((eventLength // 2) + 1)]
        
        firstHalf = range(start, middle[0])
        firstHalf = firstHalf[::-1]
        
        secondHalf = range(middle[1],end+1)
            
        for i in firstHalf:
            if signal[i] > avg:
                signal[i] = signal[i+1] * attack                        
            
        for i in secondHalf:
            if signal[i] > avg:
                signal[i] = signal[i-1] * attack
    
    
    for pair in underClippingPairs:
        start = pair[0]
        end = pair[1]
        eventLength = end-start
        middle = []
        if (eventLength)%2==1:
            middle += [ start + ((eventLength // 2) + 1) ]        
            
        else:
            middle += [start + (eventLength // 2)]
            middle += [start + ((eventLength // 2) + 1)]
        
        firstHalf = range(start, middle[0])
        firstHalf = firstHalf[::-1]
        
        secondHalf = range(middle[1],end+1)
            
        for i in firstHalf:
            if signal[i] > avg:
                signal[i] = signal[i+1] * attack                        
            
        for i in secondHalf:
            if signal[i] > avg:
                signal[i] = signal[i-1] * attack        
        
  
      
      
      return signal  
      
      
      
      
      
      
       
       
def demo():
    
    return 0









        