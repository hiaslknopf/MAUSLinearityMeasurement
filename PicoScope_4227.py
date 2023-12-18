from picosdk.ps4000 import ps4000 as ps
from picosdk.functions import adc2mV, assert_pico_ok
import numpy as np
import ctypes

""" Collection of functions to control the PicoScope 4227 Oscilloscope

-------------------------Not finished --------------------------

This script can just stream the data from the PicoScope to the PC.
For measurements on the waveforms, you may:
- read out the raw ADC vs Timebase data from the PicoScope (blocked for x trigger events)
- Convert the ADC values to mV and add a time axis
- Find your metrics using numpy methods etc

This code is based on the following example:
https://github.com/picotech/picosdk-python-wrappers/blob/master/ps4000Examples/ps4000BlockExample.py

"""

#TODO: This is not yet finished !!! Have a look at the programming example !!!

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

def get_connection():
    # Open 5000 series PicoScope
    # Returns handle to chandle for use in future API functions
    status["openunit"] = ps.ps4000OpenUnit(ctypes.byref(chandle))
    assert_pico_ok(status["openunit"])

    pass

def setup_scope():
    """ Setup channel, trigger, range and timebase """

    # Set up channel A
    # handle = chandle
    # channel = PS4000_CHANNEL_A = 0
    # enabled = 1
    # coupling type = PS4000_DC = 1
    # range = PS4000_2V = 7
    chARange = 7
    status["setChA"] = ps.ps4000SetChannel(chandle, 0, 1, 1, chARange)
    assert_pico_ok(status["setChA"])

    # Set up single trigger
    # handle = chandle
    # enabled = 1
    # source = PS4000_CHANNEL_A = 0
    # threshold = 1024 ADC counts
    # direction = PS4000_RISING = 2
    # delay = 0 s
    # auto Trigger = 1000 ms
    status["trigger"] = ps.ps4000SetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 1000)
    assert_pico_ok(status["trigger"])

    # Set number of pre and post trigger samples to be collected
    preTriggerSamples = 2500
    postTriggerSamples = 2500
    maxSamples = preTriggerSamples + postTriggerSamples
    pass

def get_data():
    """ Buffer one block of data from the scope and return it as a numpy array """
    pass
