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
            newaudio = AudioSegment.from_mp3(audio)
            newaudio.export(audio, format="wav")
            return audio
        else:
            return audio
        

    def set_channels(self, audio):
        num_channels = audio.channels
        if num_channels == 1:
            return audio
        else:
            raw_audio = AudioSegment.from_file(audio, format="wav")
            mono_wav = raw_audio.set_channels(1)
            mono_wav.export(audio, format="wav")
            return mono_wav

    def find_target_freq(freqs):  # find a mid-range frequency
        for x in freqs:
            if x > 1000:
                break
        return x

    def calculate_frequency(self, audio):
        sample_rate, data = wavfile.read(audio)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(audio, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        target_frequency = self.find_target_freq()
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]  # find index of target_frequency
        # find a sound data for a particular frequency
        data_for_frequency = self.spectrum[index_of_frequency]
        # change a digital signal for values in decibels
        self.frequency = 10 * np.log10(data_for_frequency)  # use natural logarithm to get more audio-natural output