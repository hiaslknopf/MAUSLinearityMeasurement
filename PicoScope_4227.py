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

def get_connection():

    return scope
    raise NotImplementedError

def setup(scope, channel, trigger, timebase, voltage_range):
    raise NotImplementedError

def run_block_acq(scope):

    return voltage, time
    raise NotImplementedError

def run_streaming_acq(scope):

    return voltage, time
    raise NotImplementedError

def close_scope(scope):
    raise NotImplementedError