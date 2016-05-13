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
import copy
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('../Utilities')
import utilities as ut
import vocoder as vo

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


def kernelGenerator(signal, threshold=.1):
    mx = max(signal)
    
    i = 0
    while signal[i] != mx:
        i += 1
    
    H = i
    signal = signal[H:]
    
    i = 0
    lowerThreshold = mx * threshold
    while signal[i] > lowerThreshold:   
        i += 1
    E = i
    signal = signal[:E]
    
    K = 1/mx    
    model = [K*sample for sample in signal]
    
    for x in range(len(model)):
        assert( model[x] <= 1 )  

    return model


#______________________________________________________________________________


def convReverb(signal, model, trim = True):
    """fileName: name of file in string form """    
    
    signal = [int(x) for x in signal]
    avg = ut.signalAvg(signal)[0]
    
    if trim: #trim to 10 seconds  
        signal = signal[:441000] 
    
    outputSignal = copy.deepcopy(signal)     
    outputSignal += [0 for x in range(len(model))]
    
    for i in range(len(signal)):
        currentSample = signal[i]
        for x in range(1, len(model)):
            index = i + x
            outputSignal[index] += currentSample * model[x]
    
    while ut.signalAvg(outputSignal)[0] > avg:
        outputSignal = [x*.9 for x in outputSignal]
               
    
    outputSignal = np.array(outputSignal)
    outputSignal = vo.vocoder(outputSignal,P=.5)
    outputSignal = np.ndarray.tolist(outputSignal) 
    outputSignal = [int(x) for x in outputSignal]
    
    

    return outputSignal
    

def convReverbDemo():
    
    #____________________
#     jfk        = ut.readWaveFile(dirIn + "jfk.wav")

    
    #____________________
    
    
    ####
    
    
    #____________________
    piano        = ut.readWaveFile(dirIn+"piano.wav")
    CAS          = ut.readWaveFile(dirIn+"Reverb_Samples/Cas.wav")
    CASmodel     = kernelGenerator(CAS)    
    
    pianoConvReverb = convReverb(piano, CASmodel, trim=False)
    
    ut.writeWaveFile(dirOut + "Piano_Conv_Reverb.wav", pianoConvReverb)
    #____________________
    
    print("Convolution Reverb Demo Complete.")


convReverbDemo()
