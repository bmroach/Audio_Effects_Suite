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
        
def reverb(signal, preDelay = 0, Decay = 1, trim = True):
    """fileName: name of file in string form
        preDelay: delay before reverb begins (seconds)
        Decay: hang time of signal (seconds)        
    """    
    signal = [int(x) for x in signal]
    
    pdSamples = preDelay * sampleRate
    dSamples = Decay * sampleRate
    
    if trim: #trim to 10 seconds  
        signal = signal[:4410]
#         signal = signal[:441000]
        
    preLength = len(signal)
        
    #pad for reverb extension 
    signal += [0 for x in range(pdSamples + dSamples)]
    
    length = len(signal)
    avg = ut.signalAvg(signal)[0]
    
    logArray = [(math.e**(-1*(x/dSamples))) for x in range(dSamples)]
    
    for i in range(preLength):
        currentSample = signal[i]
        for x in range(dSamples): 
            index = i + x + pdSamples #account for predelay
            
            signal[index] = signal[index] + (currentSample * logArray[x])
             
    goalAmp = avg * 1.2        
    while ut.signalAvg(signal)[0] > goalAmp:
        signal = [x*.90 for x in signal]
     
    signal = [int(x) for x in signal]
     
    return signal 




def reverbDemo():
    
        
#     obama       = ut.readWaveFile(dirIn+"ObamaAcceptanceSpeech.wav")
#     obamaReverb = reverb(obama)
#     ut.writeWaveFile(dirOut + "Obama_Distortion.wav", obamaDist)
    
#     jfk        = ut.readWaveFile(dirIn + "jfk.wav")
#     jfkReverb  = reverb(jfk)
#     ut.writeWaveFile(dirOut + "JFK_Distortion.wav", jfkDist)

    piano       = ut.readWaveFile(dirIn+"piano.wav")
    pianoReverb = reverb(piano)
    ut.writeWaveFile(dirOut + "Piano_Reverb.wav", pianoReverb)
    
    print("Reverb Demo Complete.")


reverbDemo()

         
        
   

