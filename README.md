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

TODO:
* Pulser calibration GUI
* Better triggering and more thorough analysis for pulser calibration
* The current .JOB file is just a placeholder for testing (Not sure if ever needed)

Ressources:
* TGF4000 Series Instruction Manual: Chapter 24+25
* PicoScope4000 Series Programmer's Guide
* GitHub: picosdk Python wrapper + examples (https://github.com/picotech/picosdk-python-wrappers)
* ORTEC MEASTRO User Manual: Chapter 6