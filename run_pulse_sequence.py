import numpy as np

import Pulser_TGF4242

""" Script to run a sequence of triangular pulses with the TGF4242 pulser """

#TODO: Set this up properly - Also with better log file

pulser = Pulser_TGF4242.get_connection(ip_adress='169.254.97.29')

save_dir = 'output' #For the log file
#voltages = np.linspace(250, 1000, 4) #in mV, Beware: step+1
voltages = [100]
acq_time = 5000 #in seconds, per voltage

Pulser_TGF4242.setup_triangular(pulser, channel=1, symm='right')
Pulser_TGF4242.run_sequence(pulser, voltages=voltages, acq_time=acq_time)

with open (f'{save_dir}/pulse_voltages.txt', 'w') as f:
    f.write('Input pulse voltages in mV:')
    f.write(str(voltages))

pulser.close()