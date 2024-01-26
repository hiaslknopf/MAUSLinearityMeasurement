import PicoScope_4227 as Scope
import Pulser_TGF4242 as Pulser

import pyvisa
import numpy as np
import pickle
import matplotlib.pyplot as plt

################################################
################# CONTROL PANEL ################
################################################

voltages = np.arange(0, 1000, 10) #Voltages in mV
num_acq = 5 # Acquisitions per voltage in s

output_name = 'test' #Name of output files (pickle, csv)

save_raw_data = True #Save raw data as pickle file
testplot_analysis = True #Plot analysis of one voltage
testplot_results = True #Plot results

################################################
################################################
################################################

data_dict = {}

# Get connected
status, chandle = Scope.get_connection()
pulser = Pulser.get_connection()

# Set up Scope
info_dict = Scope.setup(status, chandle, channel='A', coupling='DC', voltage_range='500mV',
                                 timebase='4ns', trigger=20, preTriggerSamples=1000, postTriggerSamples=1000)

# Set up Pulser
Pulser.setup_triangular(pulser, channel=1)

# Run pulser and scope for a given number of acquisitions
for volt in voltages:
    Pulser.run_single_volt(pulser, volt)

    voltage_data = [] #One list per voltage with num_acq elements each
    time_data = [] #TODO: Maybe time is the same for all voltages? Dann musst nicht so viel speichern

    for i in range(num_acq):
        volt_new, time_new = Scope.run_block_acq(status, chandle, channel='A', info_dict=info_dict)
        voltage_data.append(volt_new)
        time_data.append(time_new)

    Pulser.stop_run(pulser)

    data_dict[volt] = {'voltage_data': voltage_data, 'time_data': time_data}

if save_raw_data:
    with open(f'{output_name}_raw_data.pickle', 'wb') as f:
        pickle.dump(data_dict, f)
        print(f'Raw data saved to file {f.name}')

# Close connections
Scope.close_scope(status, chandle)
pulser.close()
    
# Analyse the data
for volt in data_dict.keys():

    max_array = [] #Temporary storage for max and min values per voltage
    min_array = []

    for acq in range(len(data_dict[volt])):
        analysis_volt = data_dict[volt][acq]
        analysis_time = data_dict[volt][acq]

        max_array.append(np.max(analysis_volt))
        min_array.append(np.min(analysis_volt))

        if testplot_analysis:
            plt.plot(analysis_time, analysis_volt, label='Waveform')
            plt.axhline(y=volt, color='k', linestyle='--', label='Set voltage')
            plt.axhline(y=np.max(analysis_volt), color='r', linestyle='--', label='Max')
            plt.axhline(y=np.min(analysis_volt), color='b', linestyle='--', label='Min')
            plt.legend()
            plt.xlabel('Time [ns]')
            plt.ylabel('Voltage [mV]')
            plt.title(f'Testplot - Voltage {volt} mV - Acquisition {acq}')
            plt.show()
    
    data_dict[volt]['avg_max'] = np.mean(max_array)
    data_dict[volt]['avg_min'] = np.mean(min_array)
    data_dict[volt]['avg_max_sigma'] = np.std(max_array)
    data_dict[volt]['avg_min_sigma'] = np.std(min_array)

# Write results to pulser calibration file (csv)
#TODO: Match format with uDos suite
with open(f'{output_name}.csv', 'w') as f:
    f.write('Voltage [mV],Measured voltage [mV],Error [mV]\n')
    for volt in voltages:
        f.write(f'{volt},{data_dict[volt]["avg_max"]},{data_dict[volt]["avg_max_sigma"]}\n')
    print(f'Results saved to file {f.name}')
    
# Optional results plot
#TODO: Match format with uDos suite
if testplot_results:
    plt.errorbar(voltages, [data_dict[volt]['avg_max'] for volt in voltages], yerr=[data_dict[volt]['avg_max_sigma'] for volt in voltages], label='Max')
    plt.plot(x=np.arange(0, 1000, 1), y=np.arange(0, 1000, 1), color='k', linestyle='--', label='Ideal response')
    plt.xlabel('Set voltage [mV]')
    plt.ylabel('Measured voltage [mV]')
    plt.title('Testplot - Pulser Calibration')
    plt.legend()
    plt.show()