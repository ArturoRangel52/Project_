import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.root = self.view.root

        self.label = ttk.Label(text="Enter Audio Sample: ")
        self.label.grid(row=1, column=0)

        # open button
        self.open_button = ttk.Button(text='Open File', command=self.select_file)
        self.open_button.grid(row=1, column=1, padx=10)

        # message
        self.message_label = ttk.Label(text='File Name: ')
        self.message_label.grid(row=1, column=2, sticky=tk.E)

        self.set_model(model)

        # Graph
        self.label = ttk.Label(text='Graphs')
        self.label.grid(row=6, column=0)
        # Plot Button
        self.open_button = ttk.Button(text='All Frequencies', command=self.model.graph_Reverberation)
        self.open_button.grid(row=6, column=1, padx=10)
        # Waveform
        self.open_button = ttk.Button(text='View Waveform', command=self.model.graph_waveform)
        self.open_button.grid(row=6, column=2, padx=10)
        # Low Frequency
        self.open_button = ttk.Button(text='Low Frequency', command=self.model.graph_low_frequency)
        self.open_button.grid(row=6, column=3, padx=10)
        # Mid Frequency
        self.open_button = ttk.Button(text='Mid Frequency', command=self.model.graph_mid_frequency)
        self.open_button.grid(row=6, column=4, padx=10)
        # High Frequency
        self.open_button = ttk.Button(text='High Frequency', command=self.model.graph_high_frequency)
        self.open_button.grid(row=6, column=5, padx=10)
        # Spectrogram
        self.open_button = ttk.Button(text='Spectrogram', command=self.model.graph_spectrogram)
        self.open_button.grid(row=6, column=6, padx=10)

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def select_file(self):
        filetypes = (('Wav files', '*.wav'), ('Mp3 files', '*.mp3'))
        self.view.filename = fd.askopenfilename(title='Open File', initialdir='/~', filetypes=filetypes)
        self.display_filedata()

    def display_filedata(self):
        self.display_filename()
        self.display_time_value()
        self.display_frequency_value()
        self.model.set_channels(self.model.convert_audio_to_wav(self.view.filename))
        self.model.initialize()
        self.display_difference()

    def display_filename(self):
        self.view.message_label = ttk.Label(text=self.model.clean_filename(self.view.filename))
        self.view.message_label.grid(row=1, column=3, sticky=tk.E)

    def display_time_value(self):
        self.model.read_audio(self.view.filename)
        self.view.message_label = ttk.Label(text='Time Value: ' + str(self.model.time_value) + ' seconds')
        self.view.message_label.grid(row=3, column=1, sticky=tk.E)

    def display_frequency_value(self):
        self.model.calculate_frequency(self.view.filename)
        self.view.message_label = ttk.Label(text='Resonant Frequency Value: ' + str(round(self.model.frequency, 2)) + ' Hz')
        self.view.message_label.grid(row=4, column=1, sticky=tk.E)

    def display_difference(self):
        self.model.calculate_difference()
        self.view.message_label = ttk.Label(text='Time Difference: ' + str(round(self.model.difference, 2)) + ' seconds')
        self.view.message_label.grid(row=5, column=1, sticky=tk.E)