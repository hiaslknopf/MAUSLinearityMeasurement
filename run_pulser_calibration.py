import PicoScope_4227 as Scope
import Pulser_TGF4242 as Pulser

import time
import numpy as np
import pickle
import matplotlib.pyplot as plt

################################################
################# CONTROL PANEL ################
################################################

pulser_ip = '169.254.97.29'

voltages = np.linspace(100, 500, 5) #Voltages in mV
num_acq = 10 # Acquisitions per voltage in s

output_name = 'output/test' #Name of output files (pickle, csv)

save_raw_data = True #Save raw data as pickle file
testplot_analysis = True #Plot analysis of one voltage
testplot_results = True #Plot results

################################################
################################################
################################################

data_dict = {}

# Get connected
status, chandle = Scope.get_connection()
pulser = Pulser.get_connection(pulser_ip)

# Set up Scope
trigger=25 #mV
info_dict = Scope.setup(status, chandle, channel='A', coupling='AC', voltage_range='1V',
                                 timebase='8ns', trigger=trigger, preTriggerSamples=1000, postTriggerSamples=10000)

# Set up Pulser
Pulser.setup_triangular(pulser, channel=1)
time.sleep(2) #Wait for pulser to settle

# Run pulser and scope for a given number of acquisitions
print('VOLTAGES', voltages)

for volt in voltages:
    Pulser.run_single_volt(pulser, volt)

    time.sleep(3) #Wait for pulser to settle	

    voltage_data = [] #One list per voltage with num_acq elements each
    time_data = [] #TODO: Maybe time is the same for all voltages? Dann musst nicht so viel speichern

    for i in range(num_acq):
        volt_new, time_new = Scope.run_block_acq(status, chandle, channel='A', info_dict=info_dict)
        voltage_data.append(volt_new)
        time_data.append(time_new)
        print(f'Acquisition {i+1}/{num_acq} for voltage {volt} mV finished')
    print('\n')

    Pulser.stop_run(pulser)

    data_dict[volt] = {'voltage_data': voltage_data, 'time_data': time_data}

    time.sleep(1) #Wait for pulser to settle

if save_raw_data:
    with open(f'{output_name}_raw_data.pickle', 'wb') as f:
        pickle.dump(data_dict, f)
        print(f'Raw data saved to file {f.name}')

# Close connections
Pulser.stop_run(pulser)
pulser.close()
Scope.close_scope(status, chandle)
    
# Analyse the data
print(data_dict.keys())

for volt in data_dict.keys():

    max_array = [] #Temporary storage for max and min values per voltage
    min_array = []
    pp_array = []

    analysis_volt = data_dict[volt]['voltage_data']
    analysis_time = data_dict[volt]['time_data']

    max_array.append(np.max(analysis_volt))
    min_array.append(np.min(analysis_volt))
    pp_array.append(np.max(analysis_volt) - np.min(analysis_volt))

    if testplot_analysis:
        for i in range(num_acq):
            plt.plot(analysis_time[i], analysis_volt[i], color='g', alpha=0.5)

        plt.axhline(y=volt, color='k', linestyle='--', label='Set voltage')
        plt.axhline(y=trigger, color='m', linestyle='--', label='Trigger')

        plt.axhline(y=np.mean(max_array), color='r', linestyle='--', label='Avg. Max')
        plt.axhline(y=np.mean(min_array), color='b', linestyle='--', label='Avg. Min')
        plt.plot(-100, np.mean(pp_array), label='Avg. Vpp = {:.2f} mV'.format(np.mean(pp_array)))

        plt.legend(loc='upper right')
        plt.xlabel('Time [ns]')
        plt.ylabel('Voltage [mV]')
        plt.title(f'Testplot - Voltage {volt} mV')
        plt.xlim(analysis_time[0][0], analysis_time[0][-1])
        plt.grid()
        plt.show()
    
    data_dict[volt]['avg_max'] = np.mean(max_array)
    data_dict[volt]['avg_min'] = np.mean(min_array)
    data_dict[volt]['avg_pp'] = np.mean(pp_array)
    data_dict[volt]['avg_max_sigma'] = np.std(max_array)
    data_dict[volt]['avg_min_sigma'] = np.std(min_array)
    data_dict[volt]['avg_pp_sigma'] = np.std(pp_array)

# Write results to pulser calibration file (csv)
#TODO: Match format with uDos suite
with open(f'{output_name}.csv', 'w') as f:
    f.write('Voltage [mV],Measured voltage [mV],Error [mV]\n')
    for volt in voltages:
        f.write(f'{volt},{data_dict[volt]["avg_max"]},{data_dict[volt]["avg_max_sigma"]}\n')
        f.write(f'{volt},{data_dict[volt]["avg_min"]},{data_dict[volt]["avg_min_sigma"]}\n')
        f.write(f'{volt},{data_dict[volt]["avg_pp"]},{data_dict[volt]["avg_pp_sigma"]}\n')
    print(f'Results saved to file {f.name}')
    
# Optional results plot
#TODO: Match format with uDos suite
if testplot_results:
    plt.errorbar(voltages, [data_dict[volt]['avg_pp'] for volt in voltages], yerr=[data_dict[volt]['avg_pp_sigma'] for volt in voltages], linestyle='--', marker='o', label='Vpp')
    plt.plot(np.arange(0, 1000, 1), np.arange(0, 1000, 1), color='k', linestyle='--', label='Ideal response')
    plt.xlabel('Set voltage [mV]')
    plt.ylabel('Measured voltage [mV]')
    plt.title('Testplot - Pulser Calibration')
    plt.grid()
    plt.legend()
    plt.show()