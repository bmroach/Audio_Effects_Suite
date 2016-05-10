"""
Filename: utilities.py

See README.md

Developed under the Apache License 2.0
"""
#______________________________________________________________________________
import array
import contextlib
import wave
import matplotlib.pyplot as plt
import numpy as np
import math
import copy



# Global parameters

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
maxAmp = (2**(8*sampleWidth - 1) - 1)    #maximum amplitude is 2**15 - 1  = 32767
minAmp = -(2**(8*sampleWidth - 1))       #min amp is -2**15

#Reference Functions

def writeWaveFile(fname, X):
    """3/22/16: untested, from ref files, should work"""    
#    fname += " w/Reverb"    
    params = [numChannels,sampleWidth, sampleRate , len(X), "NONE", None]
    data = array.array("h",X)
    with contextlib.closing(wave.open(fname, 'w')) as f:
        f.setparams(params)
        f.writeframes(data.tobytes())
    print(fname + " written.")
    

def readWaveFile(fileName,withParams=False,asNumpy=False):
    """3/22/16: untested, from ref files, should work"""
    with contextlib.closing(wave.open(fileName)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    if asNumpy:
        X = np.array(frames,dtype='int16')
    else:  
        X = array.array('h', frames)
    if withParams:
        return X,params
    else:
        return X 



def signalAvg(signal):
    """returns a double containing the avg of positive values and the avg of negative values"""
    posAvg = 0
    posCount = 0 
    negAvg = 0
    negCount = 0 
        
    for i in range(len(signal)):
        if signal[i] >= 0:
            posAvg += signal[i]
            posCount+= 1
            
        else:
            negAvg += signal[i]
            negCount += 1

    if posCount > 0:
        posAvg /= posCount
    
    if negCount > 0:    
        negAvg /= negCount        
                         
    return [posAvg, negAvg]


def signalCapPercent(signal):
    val = 0
    for i in range(len(signal)):
        if signal[i] >= maxAmp or signal[i] <= minAmp:
            val += 1     
    return val/len(signal)


        
    