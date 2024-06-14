import numpy as np
import pickle
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit

#TODO: Fit function maybe and discard badly triggered events
#TODO: Dont just take uncertainty on max but actual waveform fluctuations - Maybe filtern?

def fit_func(x, A, B, C, D, E):
      return A * np.exp(-D*x) / (1+np.exp(B * (x-C))) - E

def analyse_pulses(data_dict, output_name, testplot_analysis=False, testplot_results=False, fit=False):

    voltages = np.array(list(data_dict.keys()))
    num_acq = len(data_dict[list(data_dict.keys())[2]]['voltage_data']) #How many lists of data per voltage at first entry
    #num_acq = 5 #For testing
    print(f'Voltages measured (mV): {voltages}')
    print(f'Number of acquisitions per voltage: {num_acq}\n')

    for volt in tqdm(data_dict.keys(), desc='Analyzing data'):

        #Temporary storage for max and min values per voltage
        max_array =     []
        min_array =     []
        pp_array =      []
        fit_pp_array =  []

        analysis_volt = data_dict[volt]['voltage_data']
        analysis_time = np.multiply(data_dict[volt]['time_data'], timebase/1000)

        for i in range(num_acq):
            max_array.append(np.max(analysis_volt[i]))
            min_array.append(np.min(analysis_volt[i]))
            pp_array.append(np.max(analysis_volt[i]) - np.min(analysis_volt[i]))

            if fit:
                # Fit function
                try:
                    p0 = [max_array[i]*0.8, -850, 65, 1e-5, 2]
                    popt, pcov = curve_fit(fit_func, analysis_time[i], analysis_volt[i], p0=p0)
                    fit = fit_func(analysis_time[i], *popt)
                    #fit = fit_func(analysis_time[i], *p0)
                    #print(max_array[i], max_array[i]*0.9, popt)

                    fit_pp_array.append(np.max(fit) - np.min(fit))
                except:
                    print('Fit failed')
        
        # Get rid of outliers
        max_array = np.array(max_array)
        min_array = np.array(min_array)
        pp_array = np.array(pp_array)
        max_array = max_array[np.abs(max_array - np.mean(max_array)) < 3*np.std(max_array)]
        min_array = min_array[np.abs(min_array - np.mean(min_array)) < 3*np.std(min_array)]
        pp_array = pp_array[np.abs(pp_array - np.mean(pp_array)) < 3*np.std(pp_array)]
        if fit:
            fit_pp_array = np.array(fit_pp_array)
            fit_pp_array = fit_pp_array[np.abs(fit_pp_array - np.mean(fit_pp_array)) < 3*np.std(fit_pp_array)]

        if testplot_analysis:
            for i in range(num_acq):
                plt.plot(analysis_time[i], analysis_volt[i], color='g', alpha=0.5)
                if fit:
                    plt.plot(analysis_time[i], fit, color='r', alpha=0.5)

            plt.axhline(y=volt, color='k', linestyle='--', label='Set voltage')
            plt.axhline(y=trigger, color='m', linestyle='--', label='Trigger')

            plt.axhline(y=np.mean(max_array), color='r', linestyle='--', label='Avg. Max')
            plt.axhline(y=np.mean(min_array), color='b', linestyle='--', label='Avg. Min')
            plt.plot(-100, np.mean(pp_array), label='Avg. Vpp = {:.2f} mV'.format(np.mean(pp_array)))
            if fit:
                plt.plot(-100, np.mean(fit_pp_array), label='Avg. Fit Vpp = {:.2f} mV'.format(np.mean(fit_pp_array)))

            plt.legend(loc='upper right')
            plt.xlabel('Time [us]')
            plt.ylabel('Voltage [mV]')
            plt.title(f'Testplot - Voltage {volt} mV')
            plt.xlim(analysis_time[0][0], analysis_time[0][-1])
            plt.grid()
            plt.show()
        
        # Get mean and std of values
        data_dict[volt]['avg_max'] = np.mean(max_array)
        data_dict[volt]['avg_min'] = np.mean(min_array)
        data_dict[volt]['avg_pp'] = np.mean(pp_array)
        data_dict[volt]['avg_fit_pp'] = np.mean(fit_pp_array)
        data_dict[volt]['avg_max_sigma'] = np.std(max_array)
        data_dict[volt]['avg_min_sigma'] = np.std(min_array)
        data_dict[volt]['avg_pp_sigma'] = np.std(pp_array)
        data_dict[volt]['avg_fit_pp_sigma'] = np.std(fit_pp_array)

    # Write results to pulser calibration file (csv)
    with open(f'{output_name}.csv', 'w') as f:
        f.write('Pulser [mV],Scope [mV],Sigma [mV]\n')
        for volt in voltages:
            f.write(f'{volt},{data_dict[volt]["avg_max"]},{data_dict[volt]["avg_max_sigma"]}\n')
            f.write(f'{volt},{data_dict[volt]["avg_min"]},{data_dict[volt]["avg_min_sigma"]}\n')
            f.write(f'{volt},{data_dict[volt]["avg_pp"]},{data_dict[volt]["avg_pp_sigma"]}\n')
            f.write(f'{volt},{data_dict[volt]["avg_fit_pp"]},{data_dict[volt]["avg_fit_pp_sigma"]}\n')
        print(f'Results saved to file {f.name}')
        
    # Optional results plot
    if testplot_results:
        plt.errorbar(voltages, [data_dict[volt]['avg_pp'] for volt in voltages], yerr=[data_dict[volt]['avg_pp_sigma'] for volt in voltages], linestyle='--', marker='o', label='Vpp')
        if fit:
            plt.errorbar(voltages, [data_dict[volt]['avg_fit_pp'] for volt in voltages], yerr=[data_dict[volt]['avg_fit_pp_sigma'] for volt in voltages], linestyle='--', marker='o', label='Fit Vpp')
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

testplot_analysis = True #Plot analysis summary for every voltage
testplot_results = True #Plot results
fit = False #Fit the data with a sigmoid

data_dict = pickle.load(open(output_name, 'rb'))

# TODO: Uncomment this for new data
trigger = 10 #mV
timebase = 8 #ns
#timebase = float(data_dict['timebase'].strip('ns'))
#trigger = data_dict['trigger']

if __name__ == '__main__':
    analyse_pulses(data_dict, output_name, testplot_analysis, testplot_results, False)