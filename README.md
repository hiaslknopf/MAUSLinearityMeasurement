### Linearity + Noise Measurement Toolkit
## Using the current MedAustron Microdosimetry Equipment

This contains three collections of functions to interact with:

* The Arbitrary Waveform Gen/Pulser TGF4242
* The PicoScope 4227 Oscilloscope
* The ORTEC MAESTRO Spectrum collection software

These can be used to:

* `run_pulse_sequence.py`: Run a defined sequence of pulses for amplifier testing, linearity measurements, ...
* `GUI_Run_Sequence.py`: The same thing with an interface
* `run_pulser_calibration.py`: Run a defined sequence of pulses and measure them using the Picoscope -> Save the data in a pickle file or analyze it directly
* `Analyse_Pulser_Calibration.py`: Helper script for analysing pulser calibration data
* `MAESTRO_Job.py`: Start an standardized acquisition using Jobfiles (.JOB)

TODO:
* Better triggering and analysis for pulser calibration
* Implement a Pulser calibration GUI
* The current .JOB file is just a placeholder for testing (Not sure if ever needed)

Ressources:

* TGF4000 Series Instruction Manual: Chapter 24+25
* PicoScope4000 Series Programmer's Guide
* GitHub: picosdk Python wrapper + examples (https://github.com/picotech/picosdk-python-wrappers)
* ORTEC MEASTRO User Manual: Chapter 6