import matplotlib.pyplot as plt
import PicoScope_4227
from tqdm import tqdm

import pickle

""" Script to collect a single waveform from the PicoScope 4227 Oscilloscope """

output_name = '50mV_250mV_100s'

# Get connected and get a handle + status
status, chandle = PicoScope_4227.get_connection()

preTriggerSamples=5000
postTriggerSamples=100000

# Set up channel A for a measurement
info_dict = PicoScope_4227.setup(status, chandle, channel='A', coupling='DC', voltage_range='500mV',
                                 timebase='8ns', trigger=10, preTriggerSamples=preTriggerSamples, postTriggerSamples=postTriggerSamples)


######################################################################
################## Run a single test acquisition #####################
######################################################################

""" volt, time = PicoScope_4227.run_block_acq(status, chandle, channel='A', info_dict=info_dict)

# Plot the waveform
plt.plot(time, volt)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [mV]')
plt.show() """

######################################################################
############## Script to collect multiple waveforms ##################
######################################################################

num_acq = int(1e8)
data_dict = {}

try:
    for evt_ctr in tqdm(range(num_acq)):
        # Run a single acquisition
        volt, time = PicoScope_4227.run_block_acq(status, chandle, channel='A', info_dict=info_dict)

        data_dict['time_axis'] = time
        data_dict[evt_ctr] = volt
except KeyboardInterrupt:
    pass

# Save the data
print(f'Saving data to testdata_pico/{output_name}.pkl...\nPlease wait ...')
with open(f'testdata_pico/{output_name}.pkl', 'wb') as f:
    pickle.dump(data_dict, f)