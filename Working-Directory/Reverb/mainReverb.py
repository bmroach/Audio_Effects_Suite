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

#______________________________________________________________________________
#Start mainReverb.py

# Global parameters
dirIn = "../Original-Audio-Samples/"
dirOut = "../Output-Audio-Samples/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100
mulFactor = sampleRate * 10


#Reference Functions

def writeWaveFile(fname, X):
    """3/22/16: untested, from ref files, should work"""    
#    fname += " w/Reverb"    
    params = [numChannels,sampleWidth, sampleRate , len(X), "NONE", None]
    data = array.array("h",X)
    with contextlib.closing(wave.open(dirOut + fname, 'w')) as f:
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
        
def reverb(fileName, preDelay = 0, Decay = 0, Variation = 0, presetOn = False, preset = ""):
    """fileName: name of file in string form
        preDelay: delay befor reverb begins (seconds)
        Decay: hang time of signal (seconds)
        Variation: TBD
        
        presetOn: whether or not a pre determined set of parameters is used
        preset: if presetOn, a string containing the preset to be applied        
    """
        
    """ Version History
        3/22/16: Prototype framework in progress (current) [BMR]
        3/25/16: Decay fix [AE]
        3/26/16: Framework adjustments [BMR]
    """
    
    #convert from seconds to pre determined unit. ie mulFactor = 10 -> width = .1s
    preDelay *= mulFactor
    Decay *= mulFactor
    
    position = 0
    windowWidth = sampleRate/mulFactor    
    data = readWaveFile(fileName)
    
    #pad zeros to add room for reverb after initial termination point 
    for x in range(Decay*sampleRate + preDelay *sampleRate):
        data.append(0)
    seconds = len(data)//sampleRate
    
    #for every (sR/mF) second window
    for i in range(seconds*mulFactor):
        #capture current window        
        currentWindow = data[position:position+(windowWidth)]  
        
        #length of decay determines reach of cloned signal
        forwardPosition = copy.deepcopy(position) #marks starting sample
        
        #account for delay before reverb starts
        forwardPosition += ((windowWidth) + (preDelay * (windowWidth) )) 

        for k in range(Decay):
            #decrease amplitude of currentWindow (reverb decaying over time)
            for x in range(len(currentWindow)):
                currentWindow[x] = math.floor(currentWindow[x] * math.e**(-1*(k/Decay)))                  
         
            #add each clone sample to samples forward in time           
        for j in range(sampleRate):
            data[forwardPosition + j] += currentWindow[j]
#            if (forwardPosition + j) < len(data):        #testing without these two lines
#               data[forwardPosition + j] += currentWindow[j]

            forwardPosition += windowWidth
        
        #mark where next window will start
        position += windowWidth
         
            
    #finally, write out to .wav file
    writeWaveFile(fileName, data)
   









     
