"""
Filename: main.py

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
#Start main.py


# Global parameters
dirIn = "../Original-Audio-Samples/"
dirOut = "../Output-Audio-Samples/"

numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100

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
        
def main(fileName, preDelay = 0, Decay = 0, Variation = 0, presetOn = False, preset = ""):
    """fileName: name of file in string form
        preDelay: delay befor reverb begins (seconds)
        Decay: hang time of signal (seconds)
        Variation: TBD
        
        presetOn: whether or not a pre determined set of parameters is used
        preset: if presetOn, a string containing the preset to be applied        
    """
        
    """ Version History
        3/22/16: Prototype framework in progress (current) [BMR]
    """
    
    
        
    data = readWaveFile(fileName)
    
    #pad zeros to add room for reverb after initial termination point 
    for x in range(Decay*44100 + preDelay *44100):
        data.append(0)
    
    position = 0
    
    seconds = len(data)//44100
    
    #for every 1 second window
    for i in range(seconds):
        
        #capture current window ##and apply initial decay        
        currentWindow = data[position:position+44100] #width of 1 second, "cloned sample"
#        for x in range(len(currentWindow)):
#            currentWindow[x] = math.floor(currentWindow[x] * .5) #half the amplitude         
        
        
        #length of decay determines reach of cloned signal
        forwardPosition = copy.deepcopy(position) #marks starting sample
        forwardPosition += (preDelay * 44100) #account for delay before reverb starts
        for k in range(Decay):
                        
            #add each clone sample to samples forward in time
            for j in range(44100):
                data[forwardPosition + j] += currentWindow[j]                
                
            #decrease amplitude of currentWindow (reverb decaying over time)
            for x in range(len(currentWindow)):
                currentWindow[x] = math.floor(-1* math.log(k+1/Decay))                

            forwardPosition += 44100
        
        #mark where next 1sec window will start
        position += 44100 
    
        
    #finally, write out to .wav file
    writeWaveFile(fileName, data)
   









     