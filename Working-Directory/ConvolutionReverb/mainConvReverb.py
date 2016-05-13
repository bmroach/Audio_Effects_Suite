"""
Filename: mainConvReverb.py

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
import sys

sys.path.append('../Utilities')
import utilities as ut

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


def FFT(X, N):
    return np.fft.rfft(X, N)
    
def IFFT(X, N):
    return np.fft.ifft(X, N)
    
def convolve(X, Y):
    return np.convolve(X, Y)

#______________________________________________________________________________

def convReverb(signal, location, preDelay = 0, Decay = 1, trim = True):
    """fileName: name of file in string form
        preDelay: delay befor reverb begins (seconds)
        Decay: hang time of signal (seconds)        
    """    
    signal = [int(x) for x in signal]
    
    print("signal acquired")
        
    location = location[6610:]
    
    pdSamples = preDelay * sampleRate
    dSamples = Decay * sampleRate
    
    if trim: #trim to 10 seconds
        signal = signal[:441000]
        print("trimmed")
    
    clap = ut.readWaveFile(dirIn+"Reverb_Samples/Clap.wav")
    clap = clap[6610:]
    
    kernel1 = np.fft.fft(location) #use FFT on location sound
    kernel2 = convolve(clap,location)
    kernel3 = []
    for i in range(0, len(clap)-1):
        kernel3 += [clap[i] * location[i]]
    kernel4 = []
    for i in range(0, len(clap)-1):
        kernel4 += [location[i]-clap[i]]
    
    print("got kernel")
    '''
    new = []
    for i in signal:
        new += [int(signal[i] * kernel1[i])]
    
        
    new2 = []
    for i in signal:
        new2 += [int(signal[i] * kernel2[i])]
        
    new3 = []
    for i in signal:
        new3 += [int(signal[i] * kernel3[i])]

    #return new? is new needed?

    print("got new")
    '''
    #according to https://en.wikipedia.org/wiki/Overlap%E2%80%93add_method#The_algorithm
    #this is the way Overlap-add should work,which is an efficient way of convolving
    
    L = 44100//2
    M = int(L*1.5)
    N = 32768
    Nx = int(len(signal));
    H = FFT(kernel4,N)     #is this right?
    #H = kernel4
    i = 1

    y = [0 for x in range(1, M+Nx-1)]

    while i <= Nx:
        il = min((i+L)-1,Nx)
        #p = len(FFT(signal[i:il], N))
        yt = IFFT(FFT(signal[i:il], N) * H, N)
        k  = min(i+N-1,M+Nx-1)
        y[i:k] = y[i:k] + yt[1:(k-i+1)]   # (add the overlapped output blocks)
        i = i+L
    
    #convert back to ints
    y = np.convolve(signal, location)
    y = [int(x) for x in y]
    
    #ensure values are within short int range
    for i in range(len(y)):
        if y[i] > maxAmp:
            y[i] = maxAmp-1
        
        elif y[i] < minAmp:
            y[i] = minAmp+1    
    
    return y






def convReverbDemo():
    
        
#     obama       = ut.readWaveFile(dirIn+"ObamaAcceptanceSpeech.wav")
#     obamaReverb = reverb(obama)
#     ut.writeWaveFile(dirOut + "Obama_Distortion.wav", obamaDist)
    
#     jfk        = ut.readWaveFile(dirIn + "jfk.wav")
#     jfkReverb  = reverb(jfk)
#     ut.writeWaveFile(dirOut + "JFK_Distortion.wav", jfkDist)

    piano       = ut.readWaveFile(dirIn+"piano.wav")
    Cas = ut.readWaveFile(dirIn+"Reverb_Samples/Cas.wav")
    print("files read, now running convReverb")
    pianoConvReverb = convReverb(piano, Cas)
    ut.writeWaveFile(dirOut + "Piano_Conv_Reverb.wav", pianoConvReverb)
    
    print("Convolution Reverb Demo Complete.")


convReverbDemo()
