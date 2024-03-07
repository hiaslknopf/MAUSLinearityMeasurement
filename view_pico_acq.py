import numpy as np
import matplotlib.pyplot as plt
import pickle

""" Script to view the data collected with run_picoscope_acq.py """

data_file = 'testdata_pico/250mV_1e3.pkl'

# Load the data
with open(data_file, 'rb') as f:
    data_dict = pickle.load(f)

# Plot the data
for i in range(len(data_dict)-1):
    plt.plot(data_dict['time_axis'], data_dict[i], 'r')

    plt.title(f'PicoScope ACQ: {data_file} - Event {i}')
    plt.grid()
    plt.xlabel('Time [ns]')
    plt.ylabel('Voltage [mV]')

    plt.show()