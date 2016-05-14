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


def distortion(signal, clipThreshold = .3, attack = .9, trim=True):
    
    if trim: #trim to 10 seconds
        signal = signal[:441000]
 
    #convert to ints
    signal = [int(x) for x in signal]
    
    
    length = len(signal)
    increment = 1.01
    
    #increase gain to induce clipping
    while ut.signalCapPercent(signal) < clipThreshold:
        for i in range(length):
            signal[i] = math.floor(signal[i] * increment)
    
    avg = ut.signalAvg(signal)
    overClippingPairs = [] 
    underClippingPairs = []
    
    #mark start and ending positions of clipping
    for i in range(length):
        if signal[i] > maxAmp:
            k = i
            while signal[k] > maxAmp:
                k += 1
                if k == length:
                    break
                            
            if k != i:
                overClippingPairs += [[i,k]]
            
        elif signal[i] < minAmp:
            j = i
            while signal[j] < minAmp:
                j += 1
                if j == length:
                    break
                            
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
        
        
        if len(middle) == 1:                        
            if end+1<length:
                secondHalf = range(middle[0],end+1)        
            else:
                secondHalf = range(middle[0],length)
        
        elif len(middle) == 2:                        
            if end+1<length:
                secondHalf = range(middle[1],end+1)        
            else:
                secondHalf = range(middle[1],length)
        
                    
        for i in firstHalf:
            if signal[i] > avg:
                z = 1
                while signal[i] >= maxAmp or signal[i] <= minAmp:
                    if z == 1:
                        signal[i] = signal[i+1] * attack
                        z += 1
                    else:
                        signal[i] *= attack
            
        for i in secondHalf:
            if signal[i] > avg:
                z = 1
                while signal[i] >= maxAmp or signal[i] <= minAmp:
                    if z == 1:
                        signal[i] = signal[i-1] * attack
                        z += 1
                    else:
                        signal[i] *= attack
    
    
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
        
        
        if len(middle) == 1:                        
            if end+1<length:
                secondHalf = range(middle[0],end+1)        
            else:
                secondHalf = range(middle[0],length)
        
        elif len(middle) == 2:                        
            if end+1<length:
                secondHalf = range(middle[1],end+1)        
            else:
                secondHalf = range(middle[1],length)
                
            
        for i in firstHalf:
            if signal[i] > avg:
                z = 1
                while signal[i] >= maxAmp or signal[i] <= minAmp:
                    if z == 1:
                        signal[i] = signal[i+1] * attack
                        z += 1
                    else:                        
                        signal[i] *= attack
        for i in secondHalf:
            if signal[i] > avg:
                z = 1
                while signal[i] >= maxAmp or signal[i] <= minAmp:
                    if z == 1:
                        signal[i] = signal[i-1] * attack
                        z += 1
                    else: 
                        signal[i] *= attack        
        
    #convert back to ints
    signal = [int(x) for x in signal]
    
    #ensure values are within short int range
    for i in range(length):
        if signal[i] > maxAmp:
            signal[i] = maxAmp-1
        
        elif signal[i] < minAmp:
            signal[i] = minAmp+1       
    
            
    return signal  
      
      
      
      
      
      
       
       
def distortionDemo():
    
    
    jfk     = ut.readWaveFile(dirIn + "jfk.wav")
    jfkDist = distortion(jfk)
    ut.writeWaveFile(dirOut + "JFK_Distortion.wav", jfkDist)

    piano     = ut.readWaveFile(dirIn+"piano.wav")
    pianoDist = distortion(piano)    
    ut.writeWaveFile(dirOut + "Piano_Distortion.wav", pianoDist)
    
    print("Distortion Demo Complete.")


distortionDemo()



        