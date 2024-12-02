import librosa
import pydub
from attr import attributes
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import mutagen
import wave
from scipy.signal import welch
from blind_rt60 import BlindRT60
from scipy.signal import butter, lfilter

class Model:
    def __init__(self):
        self.sample_rate = 0
        self.data = None
        self.channels = 0
        self.freqs = None
        self.spectrum = None
        self.t = None
        self.im = None
        self.time_value = 0
        self.frequency = 0
        self.difference = 0
        self.final_audio = None

    def clean_filename(self, filename):
        newname = filename.rsplit('/', 1)[-1]
        return newname

    def read_audio(self, file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            frames = wave.open(file_path, "r").getnframes()
            rate = wave.open(file_path, "r").getframerate()
            self.time_value = round(frames / float(rate), 2)
            return audio
        except Exception as e:
            print(f"Error reading audio file: {e}")
            return None

    def convert_audio_to_wav(self, audio):
        format_ = audio.rsplit('/', 1)[-1].rsplit('.', 1)[1]
        if format_ == 'mp3':
            try:
                newaudio = AudioSegment.from_mp3(audio)
            except:
                newaudio = AudioSegment.from_file(audio)
                audio = newaudio.export(format="mp4")
                newaudio = AudioSegment.from_file(audio, format="mp4")
            audio = newaudio.export(format="wav")
            return audio
        else:
            return audio
        

    def set_channels(self, audio):
        newaudio = AudioSegment.from_wav(audio)
        num_channels = newaudio.channels
        if num_channels == 1:
            self.final_audio = audio
        else:
            mono_wav = newaudio.set_channels(1)
            mono_wav_audio = mono_wav.export(format="wav")
            self.final_audio = mono_wav_audio

    def find_target_freq(freqs):  # find a mid-range frequency
        for x in freqs:
            if x > 1000:
                break
        return x

    def calculate_frequency(self, audio):
        data, sample_rate = librosa.load(audio)
        # Apply FFT
        fft_data = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(fft_data), 1 / sample_rate)
        # Identify the resonant frequency
        magnitude = np.abs(fft_data)
        self.frequency = frequencies[np.argmax(magnitude)]

    def calculate_difference(self):
        data_in_db = self.frequency_check()
        # find index of a max value
        index_of_max = np.argmax(data_in_db)
        # for computation and marking plot
        value_of_max = data_in_db[index_of_max]
        # slice array from a max value
        sliced_array = data_in_db[index_of_max:]
        # determine 5db less of max value
        value_of_max_less_5 = value_of_max - 5
        # determine absolute value and subtract less 5 db value
        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        # slice array from a max -5db
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)  # determine -25db down
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]  # compute RT20
        # extrapolate rt20 to rt60
        rt60 = 3 * rt20  # extrapolate to RT60
        self.difference = rt60

    def initialize(self):
        self.sample_rate, self.data = wavfile.read(self.final_audio)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.sample_rate)

    def find_target_frequency(self, x):  # find a mid-range frequency
        for x in self.freqs:
            if x > 1000:
                break
        return x

    def frequency_check(self):  # choose a frequency to check
        target_frequency = self.find_target_frequency(self.freqs)
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]  # find index of target_frequency
        # find a sound data for a particular frequency
        data_for_frequency = self.spectrum[index_of_frequency]
        # change a digital signal for values in decibels
        data_in_db_fun = 10 * np.log10(data_for_frequency)  # use natural logarithm to get more audio-natural output
        return data_in_db_fun

    def find_nearest_value(self, array, value):  # pass in sliced array list and value less 5db
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()  # convert input into array
        return array[idx]