### Linearity + Noise Measurement Toolkit (MedAustron)

This contains three collections to interact with:

* The Arbitrary Waveform Gen/Pulser TGF4242
* The PicoScope 4227 Oscilloscope
* The ORTEC MAESTRO Spectrum collection software

These can be used to:

* `run_pulse_sequence.py`: Run a defined sequence of pulses for amplifier testing, linearity measurements, ...
* `GUI_Run_Sequence.py`: The same thing with an interface
* `MAESTRO_Job.py`: Start an standardized acquisition using Jobfiles (.JOB)
* Eventually run completely automated linearization or calibration measurements


TODO:

* Implement PicoScope Communication (PicoSDK)
* Fully automated pulser calibration (PicoScope + Pulser) --> csv
* The current .JOB file is just a placeholder for testing
* This has not been tested

Ressources:

* TGF4000 Series Instruction Manual: Chapter 24+25
* PicoScope4000 Series Programmer's Guide
* GitHub: picosdk Python wrapper + examples (https://github.com/picotech/picosdk-python-wrappers)
* ORTEC MEASTRO User Manual: Chapter 6
