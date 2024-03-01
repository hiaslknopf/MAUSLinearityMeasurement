import matplotlib.pyplot as plt
import PicoScope_4227

import pickle

""" Script to collect a single waveform from the PicoScope 4227 Oscilloscope """

output_name = 'test'

# Get connected and get a handle + status
status, chandle = PicoScope_4227.get_connection()

preTriggerSamples=1000
postTriggerSamples=1000

# Set up channel A for a measurement
info_dict = PicoScope_4227.setup(status, chandle, channel='A', coupling='DC', voltage_range='500mV',
                                 timebase='4ns', trigger=20, preTriggerSamples=1000, postTriggerSamples=1000)


######################################################################
################## Run a single test acquisition #####################
######################################################################

volt, time = PicoScope_4227.run_block_acq(status, chandle, channel='A', info_dict=info_dict)

# Plot the waveform
plt.plot(time, volt)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [mV]')
plt.show()

######################################################################
############## Script to collect multiple waveforms ##################
######################################################################

""" num_acq = 1e3
data_dict = {}

for evt_ctr in range(num_acq):
    # Run a single acquisition
    volt, time = PicoScope_4227.run_block_acq(status, chandle, channel='A', info_dict=info_dict)

    data_dict['time_axis'] = time
    data_dict[evt_ctr] = volt

# Save the data
with open(f'{output_name}.pkl', 'wb') as f:
    pickle.dump(data_dict, f) """