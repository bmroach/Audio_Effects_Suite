"""
Filename: main.py

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

#______________________________________________________________________________
#Start main.py


# Global parameters
dirIn = "/../Original-Audio-Samples/"
dirOut = "/../Output-Audio-Samples/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100

#Reference Functions

def writeWaveFile(fname, X):
    """3/22/16: untested, from ref files, should work"""
    params = [numChannels,sampleWidth, sampleRate , len(X), "NONE", None]
    data = array.array("h",X)
    with contextlib.closing(wave.open(dirOut + fname, "w")) as f:
        f.setparams(params)
        f.writeframes(data.tobytes())
    print(fname + " written.")
    

def readWaveFile(fileName,withParams=False,asNumpy=False):
    """3/22/16: untested, from ref files, should work"""
    with contextlib.closing(wave.open(dirIn + fileName)) as f:
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

        
#______________________________________________________________________________
        
def main(fileName, preDelay, Decay, Variation, presetOn = False, preset = ""):
    """3/22/16: Prototype framework"""
        
        
        
   









     