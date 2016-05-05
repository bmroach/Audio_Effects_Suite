"""
Filename: mainConvReverb.py

See README.md

Developed under the Apache License 2.0
"""
#______________________________________________________________________________
#Header Imports
import sys
sys.path.append('../Utilities')
import utilities as ut

import array
import contextlib
import wave
import matplotlib.pyplot as plt
import numpy as np
import math
import copy 


#______________________________________________________________________________
#Start mainConvReverb.py

# Global parameters
dirIn = "../../Original-Audio-Samples/"
dirOut = "../../Output-Audio-Samples/ConvolutionReverb/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
mulFactor = sampleRate * 10


#______________________________________________________________________________

def convReverb(signal, preDelay = 0, Decay = 1, trim = True):
    """fileName: name of file in string form
        preDelay: delay befor reverb begins (seconds)
        Decay: hang time of signal (seconds)        
    """    
    signal = [int(x) for x in signal]
    
    print("signal aquired")
        
    
    pdSamples = preDelay * sampleRate
    dSamples = Decay * sampleRate
    
    if trim: #trim to 10 seconds
        signal = signal[:441000]
    
    print("trimmed")
    '''
    signal += [0 for x in range(pdSamples + dSamples)]
    
    length = len(signal)
    avg = ut.signalAvg(signal)[0]
    
    for i in range(length):
        currentSample = signal[i]
        for x in range(dSamples): 
            index = i + x + pdSamples #account for predelay
            
            signal[index] += (currentSample * (math.e**(-1*(x/dSamples))))
            
    goalAmp = avg * 1.2        
    while ut.signalAvg(signal)[0] > goalAmp:
        signal = [x*.90 for x in signal]
        print("still going...")
    
    signal = [int(x) for x in signal]
    
    print("reverb done, now doing realFFT...")
    '''
    kernel = realFFT(signal)
    
    print("got kernel")

    new = []

    for i in signal:
        new.append(int(signal[i]) * int(kernel[i]))
        
    print("got new")
    print(signal[0])
    print(kernel[0])
    print(new[0])
    
    return new


def realFFT(X):
    return [2.0 * np.absolute(x)/len(X) for x in np.fft.rfft(X)]



def convReverbDemo():
    
        
#     obama       = ut.readWaveFile(dirIn+"ObamaAcceptanceSpeech.wav")
#     obamaReverb = reverb(obama)
#     ut.writeWaveFile(dirOut + "Obama_Distortion.wav", obamaDist)
    
#     jfk        = ut.readWaveFile(dirIn + "jfk.wav")
#     jfkReverb  = reverb(jfk)
#     ut.writeWaveFile(dirOut + "JFK_Distortion.wav", jfkDist)

    piano       = ut.readWaveFile(dirIn+"piano.wav")
    print("file read, now running convReverb")
    pianoConvReverb = convReverb(piano)
    ut.writeWaveFile(dirOut + "Piano_Conv_Reverb.wav", pianoConvReverb)
    
    print("Reverb Demo Complete.")


convReverbDemo()
