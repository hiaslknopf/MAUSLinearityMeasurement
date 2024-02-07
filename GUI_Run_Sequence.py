import numpy as np
import Pulser_TGF4242
import tkinter as tk
from tkinter import messagebox

""" Simple GUI to run a sequence of voltage pulses with the TGF4242 pulser 

    Connection via Ethernet cable -> Automatic IP assignment
    To find the instrument IP adress: UTILITY -> Help -> option3 -> Scroll down to "IP address"
"""

class PulserGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Run Pulse Sequence (TGF4242)")

        # Main Frame
        self.main_frame = tk.Frame(master, padx=20, pady=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Group 1: IP Address and Connect Button
        self.group1_frame = tk.LabelFrame(self.main_frame, text="IP Address and Connection", padx=10, pady=10)
        self.group1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.ip_label = tk.Label(self.group1_frame, text="Pulser IP Address:")
        self.ip_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.ip_entry = tk.Entry(self.group1_frame)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.connect_button = tk.Button(self.group1_frame, text="Test Connection", command=self.test_connection)
        self.connect_button.grid(row=0, column=2, padx=10, pady=5)

        # Group 2: Voltage Range and Sequence
        self.group2_frame = tk.LabelFrame(self.main_frame, text="Voltage Input [mV]", padx=10, pady=10)
        self.group2_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.from_label = tk.Label(self.group2_frame, text="From")
        self.from_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.voltage_from_entry = tk.Entry(self.group2_frame, state="disabled", width=5)  # Adjusted width here
        self.voltage_from_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.to_label = tk.Label(self.group2_frame, text="To")
        self.to_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E)

        self.voltage_to_entry = tk.Entry(self.group2_frame, state="disabled", width=5)  # Adjusted width here
        self.voltage_to_entry.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)

        self.steps_label = tk.Label(self.group2_frame, text="Steps")
        self.steps_label.grid(row=0, column=4, padx=10, pady=5, sticky=tk.E)

        self.voltage_steps_entry = tk.Entry(self.group2_frame, state="disabled", width=5)  # Adjusted width here
        self.voltage_steps_entry.grid(row=0, column=5, padx=10, pady=5, sticky=tk.W)

        self.voltage_range_button = tk.Button(self.group2_frame, text="Enable Range", command=self.enable_voltage_range)
        self.voltage_range_button.grid(row=0, column=6, padx=10, pady=5)

        self.voltage_sequence_label = tk.Label(self.group2_frame, text="Voltage Sequence\n(Comma separated)")
        self.voltage_sequence_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.voltage_sequence_entry = tk.Entry(self.group2_frame, state="disabled")
        self.voltage_sequence_entry.grid(row=1, column=1, columnspan=4, padx=10, pady=5, sticky=tk.W)

        self.voltage_sequence_button = tk.Button(self.group2_frame, text="Enable Sequence", command=self.enable_voltage_sequence)
        self.voltage_sequence_button.grid(row=1, column=6, padx=10, pady=5)

        # Group 3: Channel Selection, Waveform Selection, and Acquisition Time
        self.group3_frame = tk.LabelFrame(self.main_frame, text="Channel and Waveform Selection", padx=10, pady=10)
        self.group3_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.channel_label = tk.Label(self.group3_frame, text="Select Channel(s)")
        self.channel_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.channel_var1 = tk.IntVar()
        self.channel1_checkbox = tk.Checkbutton(self.group3_frame, text="Channel 1", variable=self.channel_var1, onvalue=1, offvalue=0)
        self.channel1_checkbox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.channel_var2 = tk.IntVar()
        self.channel2_checkbox = tk.Checkbutton(self.group3_frame, text="Channel 2", variable=self.channel_var2, onvalue=2, offvalue=0)
        self.channel2_checkbox.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

        self.waveform_label = tk.Label(self.group3_frame, text="Select Waveform")
        self.waveform_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.waveform_var = tk.StringVar()
        self.waveform_var.set("Triangular")

        self.triangular_button = tk.Radiobutton(self.group3_frame, text="Triangular", variable=self.waveform_var, value="Triangular")
        self.triangular_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.sine_button = tk.Radiobutton(self.group3_frame, text="Sine", variable=self.waveform_var, value="Sine")
        self.sine_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        self.square_button = tk.Radiobutton(self.group3_frame, text="Square", variable=self.waveform_var, value="Square")
        self.square_button.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)

        self.acq_time_label = tk.Label(self.group3_frame, text="Acquisition Time per voltage [s]")
        self.acq_time_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.acq_time_entry = tk.Entry(self.group3_frame, width=5)
        self.acq_time_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky=tk.W)

        # Group 4: Run Button
        self.group4_frame = tk.Frame(self.main_frame)
        self.group4_frame.grid(row=3, column=0, padx=10, pady=10)

        self.run_button = tk.Button(self.group4_frame, text="Run Pulser", command=self.run_pulser, width=20, height=2)
        self.run_button.grid(row=0, column=0, pady=10, padx=10)

    def test_connection(self):
        ip_address = self.ip_entry.get()
        print('ip_address: ', ip_address)
        try:
            pulser = Pulser_TGF4242.get_connection(ip_adress=ip_address) # <--------------------------------- Connection function gets called here
            pulser.close()
            messagebox.showinfo("Connection Test", "Connection successful!")
        except Exception as e:
            messagebox.showerror("Connection Test", f"Error: {str(e)}")

    def enable_voltage_range(self):
        self.voltage_from_entry.config(state="normal")
        self.voltage_to_entry.config(state="normal")
        self.voltage_steps_entry.config(state="normal")
        self.voltage_sequence_entry.config(state="disabled")

    def enable_voltage_sequence(self):
        self.voltage_from_entry.config(state="disabled")
        self.voltage_to_entry.config(state="disabled")
        self.voltage_steps_entry.config(state="disabled")
        self.voltage_sequence_entry.config(state="normal")

    def run_pulser(self):
        ip_address = self.ip_entry.get()
        print('ip_address: ', ip_address)

        try:
            if self.voltage_from_entry.get() and self.voltage_to_entry.get():
                voltages = np.linspace(float(self.voltage_from_entry.get()), float(self.voltage_to_entry.get()), int(self.voltage_steps_entry.get())+1)
                if voltages[-1] > 1000:
                    messagebox.showwarning("Run Pulser", "Maximum voltage is 1000mV.")
                    raise ValueError("Maximum voltage is 1000mV.")
                    
                if voltages[0] < 1:
                    messagebox.showwarning("Run Pulser", "Minimum voltage is 1mV.")
                    raise ValueError("Minimum voltage is 1mV.")
                if float(self.voltage_from_entry.get()) > float(self.voltage_to_entry.get()):
                    messagebox.showwarning("Run Pulser", "Voltage range is invalid.")
                    raise ValueError("Voltage range is invalid.")
                
                print('voltages: ', voltages)
            elif self.voltage_sequence_entry.get():
                voltages = np.array(list(map(int, self.voltage_sequence_entry.get().split(','))))
                voltages = sorted(voltages)
                print('voltages: ', voltages)
            else:
                raise ValueError("Please enter voltage range or sequence.")

            pulser = Pulser_TGF4242.get_connection(ip_adress=ip_address) # <--------------------------------- Connection function gets called here

            wfm = self.waveform_var.get().lower()
            channels = []
            if self.channel_var1.get() == 1:
                channels.append(1)
            if self.channel_var2.get() == 2:
                channels.append(2)

            for channel in channels:
                print('Channel: ', channel)
                if wfm == "triangular":
                    print('Waveform: ', wfm)
                    waveform_function = Pulser_TGF4242.setup_triangular(pulser, channel) # <--------------------------------- Setup function gets called here
                elif wfm == "sine":
                    print('Waveform: ', wfm)
                    waveform_function = Pulser_TGF4242.setup_sine(pulser, channel) # <--------------------------------- Setup function gets called here
                elif wfm == "square":
                    print('Waveform: ', wfm)
                    waveform_function = Pulser_TGF4242.setup_square(pulser, channel) # <--------------------------------- Setup function gets called here

            acq_time = float(self.acq_time_entry.get()) if self.acq_time_entry.get() else 5 #Default=5s
            print('\nacq_time: ', acq_time)

            Pulser_TGF4242.run_sequence(pulser, voltages=voltages, acq_time=acq_time) # <--------------------------------- Run sequence function gets called here

            pulser.close() # <--------------------------------- Connection gets closed here

            messagebox.showinfo("Run Pulser", "Pulser run successful!")
        except ValueError as ve:
            messagebox.showerror("Run Pulser", f"Error: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Run Pulser", f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PulserGUI(root)
    root.mainloop()


