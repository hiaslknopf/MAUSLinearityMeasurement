import matplotlib.pyplot as plt
import PicoScope_4227

""" Script to collect a single waveform from the PicoScope 4227 Oscilloscope """

# Get connected and get a handle + status
status, chandle = PicoScope_4227.get_connection()

# Set up channel A for a measurement
info_dict = PicoScope_4227.setup(status, chandle, channel='A', coupling='DC', voltage_range='500mV',
                                 timebase='4ns', trigger=20, preTriggerSamples=1000, postTriggerSamples=1000)

# Run a single acquisition
volt, time = PicoScope_4227.run_block_acq(status, chandle, channel='A', info_dict=info_dict)

print(volt)

# Plot the waveform
plt.plot(time, volt)
plt.xlabel('Time [ns]')
plt.ylabel('Voltage [mV]')
plt.show()