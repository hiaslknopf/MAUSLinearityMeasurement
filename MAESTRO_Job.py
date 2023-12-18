import shutil
import os
import subprocess

""" Its possible to run ORTEC MAESTRO automatically via .JOB files (Manual Ch.6, p101ff)
    This script copies a .JOB file from the current directory into the Maestro folder
    and starts the measurement described in it.

    In order to use this, the main code has to be run as an administrator to get access to the MAESTRO folder.
"""

jobfile = 'Testjob.JOB'
maestro_folder = 'C:\Program Files (x86)\Maestro\jobs'

# ------------------------------------------------------------------------------

def move_jobfile(jobfile, maestro_folder):
    """ Copies the jobfile into the maestro folder"""

    if not os.path.exists(maestro_folder):
        raise FileNotFoundError(f'Could not find Maestro folder at {maestro_folder}')

    if not os.path.exists(f'{maestro_folder}\jobs'):
        os.makedirs(f'{maestro_folder}\jobs')

    # Copy the job file into the Maestro folder
    shutil.copy(jobfile, f'{maestro_folder}\jobs')

def start_maestro(jobfile, maestro_folder):
    """ Starts the measurement described in the jobfile"""

    # Start the measurement
    os.chdir(maestro_folder)
    subprocess.call(['Mca32.exe', jobfile])

if __name__ == '__main__':
    
    move_jobfile(jobfile, maestro_folder)
    start_maestro(jobfile, maestro_folder)

    print(f'Started MAESTRO with jobfile {jobfile}')
