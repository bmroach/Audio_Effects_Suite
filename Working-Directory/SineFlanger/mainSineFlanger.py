"""
Filename: mainSineFlanger.py

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
dirOut = "../../Output-Audio-Samples/SineFlanger/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
mulFactor = sampleRate * 10


#______________________________________________________________________________
        
def sineFlanger(signal, constant = 100,prefix = 1000, plot = False):
        
    length = len(signal)
    signal1 = [x*.5 for x in signal]
    signal2 = [x*.5 for x in signal]
    
    outputSignal = []
    valList = []
    
    for i in range(length):
        val = int(prefix * (math.sin(i/constant)))
        if i < length-val:
            outputSignal += [(signal1[i]+ signal2[val])]            
            if plot and i < 100:            
                valList += [val]
                
        else:
            outputSignal += [ (signal1[i] * 2) ]
        
    
    outputSignal = np.array(outputSignal)
    outputSignal = vo.vocoder(outputSignal,P=.5)
    outputSignal = np.ndarray.tolist(outputSignal)         
    outputSignal = [int(x) for x in outputSignal]
    
    if plot:
        plt.plot(valList)
    
    return outputSignal




def sineFlangerDemo():
    
    jfk = ut.readWaveFile(dirIn+"jfk.wav")
    jfksFlanger = sineFlanger(jfk, plot=True)
    ut.writeWaveFile(dirOut + "JFK_SineFlanger.wav", jfksFlanger)
    
#    piano = ut.readWaveFile(dirIn+"piano.wav")
#    pianosFlanger = sineFlanger(piano)
#    ut.writeWaveFile(dirOut + "Piano_SineFlanger.wav", pianosFlanger)
#    
#    violin = ut.readWaveFile(dirIn+"Violin2.wav")
#    violinsFlanger = sineFlanger(violin)
#    ut.writeWaveFile(dirOut + "Violin_SineFlanger.wav", violinsFlanger)
    
    
    print("Sine_Flanger Demo Complete.")


sineFlangerDemo()        





        
        