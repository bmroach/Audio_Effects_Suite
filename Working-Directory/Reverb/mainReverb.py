"""
Filename: mainReverb.py

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
#Start mainReverb.py

# Global parameters
dirIn = "../../Original-Audio-Samples/"
dirOut = "../../Output-Audio-Samples/Reverb/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
        
#______________________________________________________________________________
        
def reverb(signal, preDelay = 0, Decay = .25, trim = True):
    """fileName: name of file in string form
        preDelay: delay before reverb begins (seconds)
        Decay: hang time of signal (seconds)        
    """    
    signal = [int(x) for x in signal]
    
    pdSamples = int(preDelay * sampleRate)
    dSamples = int(Decay * sampleRate)
    
    if trim: #trim to 10 seconds  
        signal = signal[:441000]        
     
    
    lengthIn = len(signal)
    logArray = [(math.e**(-1*(x/dSamples))) for x in range(dSamples)]
    avg = ut.signalAvg(signal)[0]
    goalAmp = avg * 1.2
    outputSignal = [0 for x in range(len(signal) + pdSamples + dSamples)]
    length = len(outputSignal)
    
    for i in range(lengthIn): #for all input samples
        currentSample = signal[i]        
        outputSignal[i] = currentSample
        
        for x in range(1,dSamples): #for all reverb samples
            index = i + x + pdSamples            
            outputSignal[index] += (currentSample * logArray[x])
                
    
    while ut.signalAvg(outputSignal)[0] > goalAmp:
        outputSignal = [x*.90 for x in outputSignal]
    
    outputSignal = [int(x) for x in outputSignal]
     
    return outputSignal 



def reverbDemo():
    
#     jfk = ut.readWaveFile(dirIn + "jfk.wav")
#     jfkReverb = reverb(jfk)
#     ut.writeWaveFile(dirOut + "JFK_Distortion.wav", jfkDist)

    piano = ut.readWaveFile(dirIn+"piano.wav")
    pianoReverb = reverb(piano)
    ut.writeWaveFile(dirOut + "Piano_Reverb.wav", pianoReverb)
    
    print("Reverb Demo Complete.")


reverbDemo()
