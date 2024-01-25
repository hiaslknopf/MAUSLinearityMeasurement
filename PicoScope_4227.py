from picosdk.ps4000 import ps4000 as ps
from picosdk.functions import adc2mV, mV2adc, assert_pico_ok
import numpy as np
import ctypes

""" Collection of functions to control the PicoScope 4227 Oscilloscope

Run get_connection() to get a connection to the PicoScope. This returns a status dictionary and a chandle.
Run setup() to set up the PicoScope (Channel, trigger, timebase). This returns a dictionary with the setup information.
Run run_block_acq() to run one block acquisition and return the voltage and time data of one trigger event as numpy arrays.
Run close_scope() to close the connection to the PicoScope after a measurement.

This code is based on the following example:
https://github.com/picotech/picosdk-python-wrappers/blob/master/ps4000Examples/ps4000BlockExample.py

"""

setup_dict = {
        'channel': {'A': 0, 'B': 1},
        'coupling': {'AC': 0, 'DC': 1},
        'voltage_range': {'10mV': 0, '20mV': 1, '50mV': 2, '100mV': 3, '200mV': 4, '500mV': 5,
                          '1V': 6, '2V': 7, '5V': 8, '10V': 9, '20V': 10, '50V': 11, '100V': 12},
        'trigger_dir': {'Above': 0, 'Below': 1, 'Rising': 2, 'Falling': 3, 'RisingOrFalling': 4},
        'timebase':  {'4ns': 0, '8ns': 1, '16ns': 2, '32ns': 3, '64ns': 4, '96ns': 5, '128ns': 6}
    }

def get_connection():

    # Create chandle and status ready for use
    chandle = ctypes.c_int16()
    status = {}

    # Open 4000 series PicoScope
    # Returns handle to chandle for use in future API functions
    status["openunit"] = ps.ps4000OpenUnit(ctypes.byref(chandle))
    assert_pico_ok(status["openunit"])

    return status, chandle

def setup(status, chandle, channel='A', coupling='AC', voltage_range='1V', trigger=None, timebase='4ns', preTriggerSamples=500, postTriggerSamples=2500):

    """ Set up one channel and trigger on the PicoScope

    Args:
        status (dict): status dictionary (return from get_connection)
        chandle (ctypes.c_int16): chandle (return from get_connection)
        channel (str): channel to be used ('A' or 'B')
        coupling (str): coupling ('AC' or 'DC')
        trigger (dict): trigger threshold in mV (Pos or negative, None for no trigger on this channel)
        timebase (int): timebase ('4ns', '8ns', '16ns', '32ns', '64ns', '96ns', '128ns')
        preTriggerSamples (int): number of samples before trigger
        postTriggerSamples (int): number of samples after trigger
        voltage_range (str): voltage range ('10mV', '20mV', '50mV', '100mV', '200mV', '500mV', '1V', '2V', '5V', '10V', '20V', '50V', '100V')
    
    """

    # Check entries
    if channel not in setup_dict['channel']:
        raise ValueError(f'Channel must be one of: {setup_dict["channel"].keys()}')
    if voltage_range not in setup_dict['voltage_range']:
        raise ValueError(f'Voltage range must be one of: {setup_dict["voltage_range"].keys()}')
    if coupling not in setup_dict['coupling']:
        raise ValueError(f'Coupling must be one of: {setup_dict["coupling"].keys()}')

    # Set up channel
    setChannel = setup_dict['channel'][channel]
    setCoupling = setup_dict['coupling'][coupling]
    setRange = setup_dict['voltage_range'][voltage_range]

    status[f"setCh{channel}"] = ps.ps4000SetChannel(chandle, setChannel, 1, setCoupling, setRange)
    assert_pico_ok(status[f"setCh{channel}"])

    # Set up trigger
    if trigger is not None:
        setTreshold = mV2adc(float(trigger['threshold']))
        
        if trigger < 0:
            setDirection = setup_dict['trigger_dir']['Falling']
        else:
            setDirection = setup_dict['trigger_dir']['Rising']

    status["trigger"] = ps.ps4000SetSimpleTrigger(chandle, 1, setChannel, setTreshold, setDirection, 0, 1000)
    assert_pico_ok(status["trigger"])

    # Set up timebase
    setTimebase = setup_dict['timebase'][timebase]
    setMaxSamples = preTriggerSamples + postTriggerSamples

    # Internal variables
    timeIntervalns = ctypes.c_float()
    returnedMaxSamples = ctypes.c_int32()
    oversample = ctypes.c_int16(1)

    status["getTimebase2"] = ps.ps4000GetTimebase2(chandle, setTimebase, setMaxSamples, ctypes.byref(timeIntervalns), oversample, ctypes.byref(returnedMaxSamples), 0)

    return {'Timebase': setTimebase, 'PreTriggerSamples': preTriggerSamples, 'PostTriggerSamples': postTriggerSamples,
            'OverSample': oversample, 'MaxSamples': setMaxSamples, 'TimeInterval': timeIntervalns.value, 'Range': setRange}

def run_block_acq(status, chandle, channel, info_dict):
    """ Run one block acquisition for a given channel on the PicoScope and return voltage and time data as numpy arrays
    
    Args:
        status (dict): status dictionary (return from get_connection)
        chandle (ctypes.c_int16): chandle (return from get_connection)
        channel (str): channel to be used ('A' or 'B')
        info_dict (dict): dictionary with setup information (return from setup function)
    """

    # Get setup information
    setChannel = setup_dict['channel'][channel]
    setRange = info_dict['Range']

    # Get timebase information
    preTriggerSamples = info_dict['PreTriggerSamples']
    postTriggerSamples = info_dict['PostTriggerSamples']
    timebase = info_dict['Timebase']
    oversample = info_dict['OverSample']
    maxSamples = info_dict['MaxSamples']
    timeIntervalns = ctypes.c_float(info_dict['TimeInterval'])

    status["runBlock"] = ps.ps4000RunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, oversample, None, 0, None, None)
    assert_pico_ok(status["runBlock"])

    # Check for data collection to finish using ps4000IsReady
    ready = ctypes.c_int16(0)
    check = ctypes.c_int16(0)
    while ready.value == check.value:
        status["isReady"] = ps.ps4000IsReady(chandle, ctypes.byref(ready))
    
    # Create buffers ready for assigning pointers for data collection
    if channel == 'A':
        bufferMax = (ctypes.c_int16 * maxSamples)()
        bufferMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
    else:
        raise ValueError(f'Channel must be one of: {setup_dict["channel"].keys()}')

    # Set data buffer location for data collection from channel selected
    status[f"setDataBuffers{channel}"] = ps.ps4000SetDataBuffers(chandle, setChannel, ctypes.byref(bufferMax), ctypes.byref(bufferMin), maxSamples)
    assert_pico_ok(status[f"setDataBuffers{channel}"])

    # create overflow loaction
    overflow = ctypes.c_int16()
    # create converted type maxSamples
    cmaxSamples = ctypes.c_int32(maxSamples)

    # Retrieve data from scope
    status["getValues"] = ps.ps4000GetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
    assert_pico_ok(status["getValues"])

    # find maximum ADC count value
    maxADC = ctypes.c_int16(32767)

    # convert ADC counts data to mV
    voltage_data =  adc2mV(bufferMax, setRange, maxADC)
    time_data = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

    return voltage_data, time_data

def close_scope(status, chandle):
    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps4000Stop(chandle)
    assert_pico_ok(status["stop"])

    # Close unit Disconnect the scope
    # handle = chandle
    status["close"] = ps.ps4000CloseUnit(chandle)
    assert_pico_ok(status["close"])

    # display status returns
    print(status)