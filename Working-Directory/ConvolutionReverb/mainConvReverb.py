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


#______________________________________________________________________________
#Start mainConvReverb.py

# Global parameters
dirIn = "../../Original-Audio-Samples/"
dirOut = "../../Output-Audio-Samples/ConvolutionReverb/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
mulFactor = sampleRate * 10
maxAmp = (2**(8*sampleWidth - 1) - 1)    #maximum amplitude is 2**15 - 1  = 32767
minAmp = -(2**(8*sampleWidth - 1))       #min amp is -2**15

#______________________________________________________________________________

def convReverb(signal, location, preDelay = 0, Decay = 1, trim = True):
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
    
    kernel = FFT(location)
    
    print("got kernel")
    
    clap = ut.readWaveFile(dirIn+"Reverb_Samples/Clap.wav")
    conv = []
    for i in range(0, len(clap)-1):
        conv.append(clap[i] * location[i])
        
    new2 = []
    for i in signal:
        new2.append(int(signal[i] * conv[i]))

    new = []

    for i in signal:
        new.append(int(signal[i] * kernel[i]))
        
    print("got new")
    
    
    L = 44100/2
    M = int(L*1.5)
    N = 32768
    Nx = len(signal);
    i = 1
    y = []
    for i in range(1, M+Nx-1):
        y.append(0)
    while i <= Nx:
        il = min(i+L-1,Nx)
        yt = IFFT( FFT(signal[i:il]) * kernel)
        k  = min(i+N-1,M+Nx-1)
        y[i:k] = y[i:k] + yt[1:k-i+1]   # (add the overlapped output blocks)
        i = i+L
    
    #convert back to ints
    y = [int(x) for x in y]
    
    #ensure values are within short int range
    for i in range(len(y)):
        if y[i] > maxAmp:
            y[i] = maxAmp-1
        
        elif y[i] < minAmp:
            y[i] = minAmp+1    
    
    return y


def FFT(X):
    return np.fft.rfft(X)
    
def IFFT(X):
    return np.fft.ifft(X)



def convReverbDemo():
    
        
#     obama       = ut.readWaveFile(dirIn+"ObamaAcceptanceSpeech.wav")
#     obamaReverb = reverb(obama)
#     ut.writeWaveFile(dirOut + "Obama_Distortion.wav", obamaDist)
    
#     jfk        = ut.readWaveFile(dirIn + "jfk.wav")
#     jfkReverb  = reverb(jfk)
#     ut.writeWaveFile(dirOut + "JFK_Distortion.wav", jfkDist)

    piano       = ut.readWaveFile(dirIn+"piano.wav")
    Cas = ut.readWaveFile(dirIn+"Reverb_Samples/Cas.wav")
    print("file read, now running convReverb")
    pianoConvReverb = convReverb(piano, Cas)
    ut.writeWaveFile(dirOut + "Piano_Conv_Reverb.wav", pianoConvReverb)
    
    print("Reverb Demo Complete.")


convReverbDemo()
