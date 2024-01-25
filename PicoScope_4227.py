from picosdk.ps4000 import ps4000 as ps
from picosdk.functions import adc2mV, mV2adc, assert_pico_ok
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

def setup_scope(range, threshold):
    """ Set up scope. Channel A: Signal, Channel B: Trigger
    
    Args:
        range (str): Voltage range of the signal channel. 
            Possible values: "10mV", "20mV", "50mV", "100mV", "200mV", "500mV", "1V", "2V", "5V", "10V", "20V", "50V", "100V", "200V", "400V", "1000V"
        treshold (int): Treshold for the trigger in mV.
    """

    range_dict = {"10mV": 0, "20mV": 1, "50mV": 2,
                  "100mV": 3, "200mV": 4, "500mV": 5,
                  "1V": 6, "2V": 7, "5V": 8, "10V": 9,
                  "20V": 10, "50V": 11, "100V": 12, "200V": 13,
                  "400V": 14, "1000V": 15}

    # Set up channel A
    # handle = chandle
    # channel = PS4000_CHANNEL_A = 0
    # enabled = 1
    # coupling type = PS4000_DC = 1
    # range = PS4000_2V = 7
    chARange = 7
    status["setChA"] = ps.ps4000SetChannel(chandle, 0, 1, 1, range_dict[range])
    assert_pico_ok(status["setChA"])

    # Set up channel B
    # handle = chandle
    # channel = PS4000_CHANNEL_A = 0
    # enabled = 1
    # coupling type = PS4000_DC = 1
    # range = PS4000_2V = 7
    chARange = 7
    status["setChB"] = ps.ps4000SetChannel(chandle, 0, 1, 1, range_dict[range])
    assert_pico_ok(status["setChB"])

    # Set up single trigger
    # handle = chandle
    # enabled = 1
    # source = PS4000_CHANNEL_B = 1
    # threshold = 1024 ADC counts
    # direction = PS4000_RISING = 2
    # delay = 0 s
    # auto Trigger = 1000 ms
    status["trigger"] = ps.ps4000SetSimpleTrigger(chandle, 1, 1, int(mV2adc(threshold)), 2, 0, 1000)
    assert_pico_ok(status["trigger"])

    # Set number of pre and post trigger samples to be collected
    preTriggerSamples = 2500
    postTriggerSamples = 2500
    maxSamples = preTriggerSamples + postTriggerSamples
    
    # Get timebase information
    # Warning: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
    # To access these Timebases, set any unused analogue channels to off.
    # handle = chandle
    # timebase = 8 = timebase
    # noSamples = maxSamples
    # pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalns)
    # pointer to maxSamples = ctypes.byref(returnedMaxSamples)
    # segment index = 0
    timebase = 8
    timeIntervalns = ctypes.c_float()
    returnedMaxSamples = ctypes.c_int32()
    oversample = ctypes.c_int16(1)
    status["getTimebase2"] = ps.ps4000GetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), oversample, ctypes.byref(returnedMaxSamples), 0)
    assert_pico_ok(status["getTimebase2"])

    # Run block capture
    # handle = chandle
    # number of pre-trigger samples = preTriggerSamples
    # number of post-trigger samples = PostTriggerSamples
    # timebase = 8 = 80 ns = timebase (see Programmer's guide for mre information on timebases)
    # time indisposed ms = None (not needed in the example)
    # segment index = 0
    # lpReady = None (using ps4000IsReady rather than ps4000BlockReady)
    # pParameter = None
    status["runBlock"] = ps.ps4000RunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, oversample, None, 0, None, None)
    assert_pico_ok(status["runBlock"])

def get_data():
    """ Buffer one block of data from the scope and return it as a numpy array """
    pass
