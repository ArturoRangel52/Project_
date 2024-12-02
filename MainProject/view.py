import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

class View:
    def __init__(self, model):
        self.filename = None
        self.message_label = None
        self.open_button = None
        self.label = None
        self.root = tk.Tk()
        self.root.title('Test')
        self.root.resizable(False, False)
        self.root.geometry('1200x700')

        self.label = ttk.Label(text="Enter Audio Sample: ")
        self.label.grid(row=1, column=0)

        #open button
        self.open_button = ttk.Button(text='Open File', command=self.select_file)
        self.open_button.grid(row=1, column=1, padx=10)

        #message
        self.message_label = ttk.Label(text='File Name: ')
        self.message_label.grid(row=1, column=2, sticky=tk.E)

        self.model = model
        self.create_widgets()
        self.target_frequency_index = 0
        self.rt60 = 0

    def set_model(self, model):
        """
        Set the controller
        :param model:
        :return:
        """
        self.model = model

    def mainloop(self):
        tk.mainloop()
    
    def create_widgets(self):
        pass
    
    def select_file(self):
        filetypes = (('Wav files', '*.wav'), ('Mp3 files', '*.mp3'))
        self.filename = fd.askopenfilename(title='Open File', initialdir='/', filetypes=filetypes)
        self.display_filedata()

    def display_filedata(self):
        self.display_filename()
        self.display_time_value()
        self.display_frequency_value()
        self.model.set_channels(self.model.convert_audio_to_wav(self.filename))
        self.model.initialize()
        self.display_difference() #possibly correct, but likely to change

    def display_filename(self):
        self.message_label = ttk.Label(text=self.model.clean_filename(self.filename))
        self.message_label.grid(row=1, column=3, sticky=tk.E)

    def display_time_value(self):
        self.model.read_audio(self.filename)
        self.message_label = ttk.Label(text='Time Value: ' + str(self.model.time_value) + ' seconds')
        self.message_label.grid(row=3, column=1, sticky=tk.E)

    def display_frequency_value(self):
        self.model.calculate_frequency(self.filename)
        self.message_label = ttk.Label(text='Resonant Frequency Value: ' + str(round(self.model.frequency, 2)) + ' Hz')
        self.message_label.grid(row=4, column=1, sticky=tk.E)

    def display_difference(self):
        self.model.calculate_difference()
        self.message_label = ttk.Label(text='Time Difference: ' + str(round(self.model.difference, 2)) + ' seconds')
        self.message_label.grid(row=5, column=1, sticky=tk.E)