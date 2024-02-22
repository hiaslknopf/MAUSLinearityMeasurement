### Linearity + Noise Measurement Toolkit
## Using the current MedAustron Microdosimetry Equipment

This contains three collections of functions to interact with:

* The Arbitrary Waveform Gen/Pulser TGF4242 (`Pulser_TGF4242.py`)
* The PicoScope 4227 Oscilloscope (`PicoScope_4227.py`)
* The ORTEC MAESTRO Spectrum collection software

These can be used as:

* `GUI_Run_Sequence.py`: Graphic interface for controlling the pulser

* `run_pulse_sequence.py`: Run a defined sequence of pulses for amplifier testing, linearity measurements, ...
* `run_pulser_calibration.py`: Run a defined sequence of pulses and measure them using the Picoscope -> Save the data in a pickle file or analyze it directly
* `run_MAESTRO_Job.py`: Start an standardized acquisition using Jobfiles (.JOB) - Probably pretty unnecessary

* `Analyse_Pulser_Calibration.py`: Helper script for analysing pulser calibration data

REQUIREMENTS:
The whole collection is Python based (3.9), Apart from standard packages you need to install:
* PicoSDK + Python Wrapper: https://github.com/picotech/picosdk-python-wrappers
* PyVISA: https://pypi.org/project/PyVISA

SETUP:
* The Pulser is connected via a direct Ethernet connection - The IP Adress is dynamically assigned and has to be changed in the source code (Usually it stays the same for the same PC)
* The PicoScope is connected via the standard USB connection - There can only be one data stream, so the PicoScope Software has to be closed when using PicoSDK !!!

RESSOURCES:
If you are confused, maybe have a look at one of the following
* TGF4000 Series Instruction Manual: Chapter 24+25
* PicoScope4000 Series Programmer's Guide
* GitHub: picosdk Python wrapper + examples (https://github.com/picotech/picosdk-python-wrappers)
* ORTEC MEASTRO User Manual: Chapter 6

  TODO:
* Pulser calibration GUI
* Better triggering and more stable analysis for pulser calibration
* The current .JOB file is just a placeholder for testing (Not sure if this functionality is ever needed)
