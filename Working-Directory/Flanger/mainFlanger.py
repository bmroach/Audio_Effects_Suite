"""
Filename: mainFlanger.py

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
import vocoder as vo

#______________________________________________________________________________
#Start mainFlanger.py

# Global parameters
dirIn = "../../Original-Audio-Samples/"
dirOut = "../../Output-Audio-Samples/Flanger/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
mulFactor = sampleRate * 10


#______________________________________________________________________________
        
def flanger(signal, delay=20):
    """delay in milliseconds"""
    
    delaySamples = int(44.1*delay)
    length = len(signal)
    signal1 = [x*.5 for x in signal]
    signal2 = copy.deepcopy(signal1)
    
    outputSignal = []
    
    for i in range(length):
        if i < length-delaySamples:
            outputSignal += [ (signal1[i]+ signal2[i+delaySamples]) ]
        else:
            outputSignal += [ (signal1[i] * 2) ]
        
    outputSignal = np.array(outputSignal)
    outputSignal = vo.vocoder(outputSignal,P=.5)
    outputSignal = np.ndarray.tolist(outputSignal)         
    outputSignal = [int(x) for x in outputSignal]
    
    return outputSignal




def flangerDemo():
    
    jfk = ut.readWaveFile(dirIn+"jfk.wav")
    jfkFlanger = flanger(jfk)
    ut.writeWaveFile(dirOut + "JFK_Flanger.wav", jfkFlanger)
    
    piano       = ut.readWaveFile(dirIn+"piano.wav")
    pianoFlanger = flanger(piano)
    ut.writeWaveFile(dirOut + "Piano_Flanger.wav", pianoFlanger)
    
    violin = ut.readWaveFile(dirIn+"Violin2.wav")
    violinFlanger = flanger(violin)
    ut.writeWaveFile(dirOut + "Violin_Flanger.wav", violinFlanger)
    
    
    print("Flanger Demo Complete.")


flangerDemo()        
        
        