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

#______________________________________________________________________________
#Start main.py


# Global parameters
dirIn = "/../Original-Audio-Samples/"
dirOut = "/../Output-Audio-Samples/"
numChannels = 1                      # mono
sampleWidth = 2                      # in bytes, a 16-bit short
sampleRate = 44100