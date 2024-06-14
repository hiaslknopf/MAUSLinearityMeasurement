import PicoScope_4227 as Scope
import Pulser_TGF4242 as Pulser
import Analyse_Pulser_Calibration as Analyse

import numpy as np
import pickle

#TODO: Set up some better trigger for low voltages - Works only well above 35mV

################################################
################# CONTROL PANEL ################
################################################

pulser_ip = '169.254.97.29'  

from_mV = 10 #Start voltage in mV
to_mV = 250 #End voltage in mV
step = 5 #Voltage step in mV

voltages = np.linspace(from_mV, to_mV, int((to_mV-from_mV)/step)+1)
voltages = np.append(voltages, [500, 750, 1000])
num_acq = 25 # Acquisitions per voltage in s

#------------------------------------------------#
save_raw_data = True #Save raw data as pickle file
analyse_directly = True #Analyse data directly after acquisition
#------------------------------------------------#

output_name = 'output/Pulser_calib_070224' #Name of output files (pickle, csv)
testplot_analysis = True #Plot analysis of one voltage
testplot_results = True #Plot results
fit = False #Fit the data with a sigmoid

################################################################################################
################################################################################################
################################################################################################

data_dict = {} #Dictionary to store all data

# Get connected
status, chandle = Scope.get_connection()
pulser = Pulser.get_connection(pulser_ip)

# Set up Scope
if np.min(voltages) < 20:
    trigger = 10 #mV
else:
    trigger=np.min(voltages)/2 #mV

# 8ns = fastest possible timebase for 4227
# Voltage range might need to be adjusted using higher pulses
# Trigger is just a simple voltage threshold

info_dict = Scope.setup(status, chandle, channel='A', coupling='AC', voltage_range='1V',
                                 timebase='8ns', trigger=trigger, preTriggerSamples=1000, postTriggerSamples=5000)

data_dict['trigger'] = trigger
data_dict['timebase'] = info_dict['Timebase']

# Set up Pulser
Pulser.setup_triangular(pulser, channel=1)

# Run pulser and scope for a given number of acquisitions
print('VOLTAGES', voltages)

for volt in voltages:
    Pulser.run_single_volt(pulser, volt)

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

# Save raw data
if save_raw_data:
    with open(f'{output_name}_cal_data.pickle', 'wb') as f:
        pickle.dump(data_dict, f)
        print(f'Raw data saved to file {f.name}')

# Close connections
Pulser.stop_run(pulser)
pulser.close()
Scope.close_scope(status, chandle)

# Analyse data
if analyse_directly:
    Analyse.analyse_pulses(data_dict, output_name, testplot_analysis, testplot_results, fit)
    print('Analysis finished')