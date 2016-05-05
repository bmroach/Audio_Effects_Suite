"""
Filename: mainPhaser.py

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
#Start mainPhaser.py

# Global parameters
dirIn = "../../Original-Audio-Samples/"
dirOut = "../../Output-Audio-Samples/Phaser/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100


#______________________________________________________________________________
        
def phaser(signal, ratio = .5, trim = True):

    signal = [int(x) for x in signal]

    if trim:
        signal = signal[:44100]
    
    length = len(signal)
    
    signal1 = [ratio*x for x in signal]
    signal2 = [(1-ratio)*x for x in signal]
    
    signal2_modified = []
    
    
    
    
    
    
    
         
    outputSignal = []
    for i in range(length):
        outputSignal += [signal1[i] + signal2_modified[i]]
     
    return outputSignal 




def phaserDemo():
    
#     obama       = ut.readWaveFile(dirIn+"ObamaAcceptanceSpeech.wav")
#     obamaPhaser = phaser(piano)
#     ut.writeWaveFile(dirOut + "Piano_Phaser.wav", obamaPhaser)

#     jfk       = ut.readWaveFile(dirIn+"jfk.wav")
#     jfkPhaser = phaser(jfk)
#     ut.writeWaveFile(dirOut + "JFK_Phaser.wav", jfkPhaser)

    piano       = ut.readWaveFile(dirIn+"piano.wav")
    pianoPhaser = phaser(piano)
    ut.writeWaveFile(dirOut + "Piano_Phaser.wav", pianoPhaser)
    
    print("Phaser Demo Complete.")


phaserDemo()
        
        
        
        