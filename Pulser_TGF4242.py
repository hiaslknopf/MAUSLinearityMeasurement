import pyvisa
import numpy as np
import time
from tqdm import tqdm

import sys

""" Script to control the TGF4242 pulser for a linearization measurement.

    Communication via VISA interface - No drivers needed
    Connection via point to point Ethernet -> Automatic IP assignment (DHCP)
    To get the instrument IP adress: UTILITY -> Help -> option3 -> Scroll down to "IP address"
"""

DEFAULT_IP = '169.254.97.29'

def get_connection(ip_adress):
    """ Establishes a connection to the TGF4242 pulser and returns the pyvisa object"""

    try:
        rm = pyvisa.ResourceManager()
        tgf4242 = rm.open_resource(f'TCPIP0::{ip_adress}::9221::SOCKET')
        tgf4242.timeout = 10000 #Set timeout to 10s
    except pyvisa.errors.VisaIOError:
        raise ConnectionError('Could not connect to TGF4242 Pulser')
    
    tgf4242.write('FREQ 1000') # Just do something to check if connection is working
    #idn = tgf4242.query('*IDN?')
    #print('Hello, I am {}\n'.format(idn))
    print('connected - Frequency set to 1000Hz\n')

    return tgf4242

def setup_triangular(tgf4242, channel, symm='left'):
    """ Sets up the TGF4242 pulser to output a triangular waveform (for PreAmp Input testing) """

    tgf4242.write('*RST') #Reset to default settings
    tgf4242.write('CHN {}'.format(channel)) #Output channel

    tgf4242.write('WAVE RAMP') #Type Maximum
    tgf4242.write('FREQ 1000') #Frequency in Hz

    tgf4242.write('LOLVL 0') #Low level amplitude = 0
    tgf4242.write('HILVL 0.01') #Set initial amplitude to 10mV
    tgf4242.write('DCOFFS 0') #DC offset 0V

    tgf4242.write('ZLOAD 50') #Load impedance 50Ohm --> 50Ohm termination on osci !!!

    if symm == 'left':
        tgf4242.write('RMPSYMM 0') #Triangular waveform
    elif symm == 'right':
        tgf4242.write('RMPSYMM 100')

    print('Setup done')
    time.sleep(5)

def setup_square(tgf4242, channel):
    """ Sets up the TGF4242 pulser to output a square waveform """

    tgf4242.write('*RST') #Reset to default settings
    tgf4242.write('CHN {}'.format(channel)) #Output channel

    tgf4242.write('WAVE SQUARE') #Type Maximum
    tgf4242.write('FREQ 1000') #Frequency in Hz

    tgf4242.write('AMPL 0.01') #Amplitude 10mV

    """ tgf4242.write('LOLVL 0') #Low level amplitude = 0
    tgf4242.write('HILVL 0.01') #Set initial amplitude to 10mV
    tgf4242.write('DCOFFS 0') #DC offset 0V """

    tgf4242.write('ZLOAD 50') #Load impedance 50Ohm --> 50Ohm termination on osci !!!
    tgf4242.write('SQRSYMM 50') #Square waveform

    print('Setup done')
    time.sleep(5)

def setup_sine(tgf4242, channel):
    """ Sets up the TGF4242 pulser to output a sinusoidal waveform """

    tgf4242.write('*RST') #Reset to default settings
    tgf4242.write('CHN {}'.format(channel)) #Output channel

    tgf4242.write('WAVE SINE') #Type Maximum
    tgf4242.write('FREQ 1000') #Frequency in Hz

    tgf4242.write('LOLVL 0') #Low level amplitude = 0
    tgf4242.write('HILVL 0.01') #Set initial amplitude to 10mV
    tgf4242.write('DCOFFS 0') #DC offset 0V

    tgf4242.write('ZLOAD 50') #Load impedance 50Ohm --> 50Ohm termination on osci !!!
    tgf4242.write('SQRSYMM 0') #Triangular waveform

    print('Setup done')
    time.sleep(5)

def run_single_volt(tgf4242, voltage):
    """ Runs a single voltage on the TGF4242 pulser for an indefinite amount of time """

    print(f'\n------ Running voltage {voltage} Vpp -------\n')

    #WARNING: Peak to Peak voltage is double the amplitude you set for some reason !!!
    voltage = voltage/2000 #Convert to V

    tgf4242.write('AMPL {}'.format(voltage)) #Set voltage

    tgf4242.write('OUTPUT ON') #Turn on output
    tgf4242.write('BEEP') #Beep when starting a run

def stop_run(tgf4242):
    """ Stops the current run on the TGF4242 pulser """

    tgf4242.write('OUTPUT OFF') #Turn off output
    tgf4242.write('BEEP') #Beep when stopping a run

def run_sequence(tgf4242, voltages, acq_time):

    #WARNING: Peak to Peak voltage is double the amplitude you set for some reason !!!
    voltages = np.divide(voltages, 2000) #Convert to V
    
    print(f'\n------ Run sequence -------\n')
    
    for volt in voltages:
        tgf4242.write('AMPL {}'.format(volt)) #Set voltage

        tgf4242.write('OUTPUT ON') #Turn on output
        tgf4242.write('BEEP') #Beep when changing voltage

        time.sleep(0.5) #Wait for the pulser to settle

        begin = time.time()
        #time.sleep(acq_time) #In seconds
        for _ in tqdm(range(int(acq_time)),desc=f"Running pulser at {volt*2000} mV..."):
            time.sleep(1)

        tgf4242.write('OUTPUT OFF') #Turn off output

        print(f'Voltage {volt*2000} mVpp finished - {time.time()-begin:.2f}s')

    for _ in range(3): tgf4242.write('BEEP') #Beep three times when finished with a run

    print(f'\n------ Sequence finished -------\n\n')

if __name__ == '__main__':

    #rm = pyvisa.ResourceManager()
    #rm.list_resources("?*::SOCKET")
    #sys.exit()

    tgf4242 = get_connection(DEFAULT_IP)
    tgf4242.close()
