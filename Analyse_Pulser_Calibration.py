import numpy as np
import pickle
import matplotlib.pyplot as plt
from tqdm import tqdm

#TODO: Fit function maybe and discard badly triggered events
#TODO: Dont just take uncertainty on max but actual waveform fluctuations

def analyse_pulses(data_dict, output_name, testplot_analysis=False, testplot_results=False):

    voltages = np.array(list(data_dict.keys()))
    num_acq = len(data_dict[list(data_dict.keys())[2]]['voltage_data']) #How many lists of data per voltage at first entry
    print(f'Voltages measured (mV): {voltages}')
    print(f'Number of acquisitions per voltage: {num_acq}\n')

    for volt in tqdm(data_dict.keys(), desc='Analyzing data'):

        max_array = [] #Temporary storage for max and min values per voltage
        min_array = []
        pp_array = []

        analysis_volt = data_dict[volt]['voltage_data']
        analysis_time = np.multiply(data_dict[volt]['time_data'], timebase/1000)

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
            plt.xlabel('Time [us]')
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

###############################################################################
##################### RUN ANALYSIS OFFLINE ####################################
###############################################################################

output_name = 'output/Pulser_calib_070224_raw_data.pickle'

testplot_analysis = False #Plot analysis summary for every voltage
testplot_results = True #Plot results

data_dict = pickle.load(open(output_name, 'rb'))

# TODO: Uncomment this for new data
trigger = 10 #mV
timebase = 8 #ns
#timebase = float(data_dict['timebase'].strip('ns'))
#trigger = data_dict['trigger']

if __name__ == '__main__':
    analyse_pulses(data_dict, output_name, testplot_analysis, testplot_results)