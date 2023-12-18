import numpy as np

import Pulser_TGF4242

""" Script to run a sequence of triangular pulses with the TGF4242 pulser """

if __name__ == "main":

    pulser = Pulser_TGF4242.get_connection(ip_adress='192.168.1.1')

    save_dir = 'output'
    voltages = np.linspace(0, 5, 100) #in mV, step+1
    acq_time = 5 #in seconds, per voltage

    Pulser_TGF4242.setup_triangular(channel=1)
    Pulser_TGF4242.run_sequence(voltages=voltages, acq_time=5)

    with open (f'{save_dir}/pulse_voltages.txt', 'w') as f:
        f.write('Input pulse voltages in mV:')
        f.write(voltages)

    pulser.close()