import pyvisa
import numpy as np
import time

""" Script to control the TGF4242 pulser for a linearization measurement.

    Connection with Ethernet cable -> Automatic IP assignment
    To find the instrument IP adress: UTILITY -> Help -> option3 -> Scroll down to "IP address"
"""

ip_adress = '169.254.97.29'

def get_connection(ip_adress):
    """ Establishes a connection to the TGF4242 pulser and returns the pyvisa object"""

    try:
        rm = pyvisa.ResourceManager()
        tgf4242 = rm.open_resource(f'TCPIP0::{ip_adress}::9221::SOCKET')
        tgf4242.timeout = 10000 #Set timeout to 10s
        print('connected')
    except pyvisa.errors.VisaIOError:
        raise ConnectionError('Could not connect to TGF4242 Pulser')
    
    #idn = tgf4242.query('*IDN?')
    #print('Hello, I am {}\n'.format(idn))
    #print('connected')

    return tgf4242

def setup_triangular(tgf4242, channel):
    """ Sets up the TGF4242 pulser to output a triangular waveform (for PreAmp Input testing)"""

    tgf4242.write('*RST') #Reset to default settings
    tgf4242.write('CHN {}'.format(channel)) #Output channel

    tgf4242.write('WAVE SQUARE') #Type Maximum
    tgf4242.write('FREQ 1000') #Frequency in Hz

    tgf4242.write('LOLVL 0') #Low level amplitude = 0
    tgf4242.write('HILVL 0.01') #Set initial amplitude to 10mV
    tgf4242.write('DCOFFS 0') #DC offset 0V

    tgf4242.write('ZLOAD 50') #Load impedance 50Ohm --> 50Ohm termination on osci !!!
    tgf4242.write('SQRSYMM 0') #Triangular waveform

    print('Setup done')

def setup_square(tgf4242, channel):
    """ Sets up the TGF4242 pulser to output a square waveform """

    tgf4242.write('*RST') #Reset to default settings
    tgf4242.write('CHN {}'.format(channel)) #Output channel

    tgf4242.write('WAVE SQUARE') #Type Maximum
    tgf4242.write('FREQ 1000') #Frequency in Hz

    tgf4242.write('LOLVL 0') #Low level amplitude = 0
    tgf4242.write('HILVL 0.01') #Set initial amplitude to 10mV
    tgf4242.write('DCOFFS 0') #DC offset 0V

    tgf4242.write('ZLOAD 50') #Load impedance 50Ohm --> 50Ohm termination on osci !!!
    tgf4242.write('SQRSYMM 50') #Square waveform

    print('Setup done')

def setup_sinusoidal(tgf4242, channel):
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

def run_sequence(tgf4242, voltages, acq_time):
    voltages = np.divide(voltages, 1000) #Convert to V
    
    for volt in voltages:
        tgf4242.write('HILVL {}'.format(volt))
        tgf4242.write('SQRSYMM 10')
        #tgf4242.write('OUTPUT ON') #Turn on output
        tgf4242.write('BEEP') #Beep when changing voltage

        begin = time.time()
        time.sleep(acq_time) #In seconds

        tgf4242.write('OUTPUT OFF') #Turn off output
        print(f'Voltage {volt} finished - {time.time()-begin:.2f}s')

    for _ in range(3): tgf4242.write('BEEP') #Beep three times when finished with a run

if __name__ == '__main__':

    tgf4242 = get_connection(ip_adress)
    tgf4242.close()
