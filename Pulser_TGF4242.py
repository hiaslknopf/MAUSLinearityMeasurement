import pyvisa
import numpy as np
import time

""" Script to control the TGF4242 pulser for a linearization measurement.

    To find the instrument IP adress: UTILITY -> Help -> option3 -> Scroll down to "IP address"
"""

ip_adress = '192.168.1.100'

def get_connection(ip_adress):
    """ Establishes a connection to the TGF4242 pulser and returns the pyvisa object"""

    try:
        rm = pyvisa.ResourceManager()
        tgf4242 = rm.open_resource(f'TCPIP0::{ip_adress}::9221::SOCKET')
    except pyvisa.errors.VisaIOError:
        raise ConnectionError('Could not connect to TGF4242 Pulser')

    idn = tgf4242.query('*IDN?')
    print('Hello, I am {}\n'.format(idn))

    return tgf4242

def setup_triangular(channel):
    """ Sets up the TGF4242 pulser to output a triangular waveform (for PreAmp Input testing)"""

    tgf4242.write('*RST') #Reset to default settings
    tgf4242.write('CHN {}'.format(channel)) #Output channel

    tgf4242.write('WAVE SQUARE') #Type Maximum
    tgf4242.write('FREQ 10000') #Frequency in Hz

    tgf4242.write('LOLVL 0') #Low level amplitude = 0
    tgf4242.write('HILVL 0.01') #Set initial amplitude to 10mV

    tgf4242.write('ZLOAD 50') #Load impedance 50Ohm --> 50Ohm termination on osci !!!
    tgf4242.write('SQRSYMM 0') #Triangular waveform

    print('Setup done')

def run_sequence(voltages, acq_time):
    voltages = np.divide(voltages, 1000) #Convert to V
    for volt in voltages:
        tgf4242.write('HILVL {}'.format(volt))
        tgf4242.write('OUTPUT ON') #Turn on output
        tgf4242.write('BEEP') #Beep when changing voltage

        time.sleep(acq_time) #In seconds
    
    tgf4242.write('OUTPUT OFF') #Turn off output
    for _ in range(3): tgf4242.write('BEEP') #Beep three times when finished

if __name__ == '__main__':

    tgf4242 = get_connection(ip_adress)

    #Close connection
    tgf4242.close()

    print('\nPulse sequence finished')
