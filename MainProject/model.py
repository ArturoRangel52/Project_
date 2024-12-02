import librosa
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import wave
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

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
        rt20 = (self.t[index_of_max_less_25] - self.t[index_of_max_less_5])[0]  # compute RT20
        # extrapolate rt20 to rt60
        rt60 = 3 * rt20  # extrapolate to RT60
        self.difference = rt60

    def initialize(self):
        self.sample_rate, self.data = wavfile.read(self.final_audio)
        self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))

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

    def graph_Reverberation(self): #copied from repo
        #Size of graph
        fig = Figure(figsize = (5, 5))
        #Data Points of graph
        xpoints = np.array([0, 6])
        ypoints = np.array([0, 250])
        #Creates a subplot
        plot1 = fig.add_subplot(111)
        plot1.set_title("Reverberation Graph")
        plot1.set_ylabel("Decibel (dB)")
        plot1.set_xlabel("Time (s)")
        #Sets MatplotLib into the tkinter window
        canvas = FigureCanvasTkAgg(fig)
        canvas.get_tk_widget().grid(row = 7, column= 4)
        canvas.draw()
        #Calls plot1 to be graphed
        plot1.plot(xpoints, ypoints)

    def graph_waveform(self):
        wav_audio = wave.open(self.final_audio, 'rb')
        n_frames = wav_audio.getnframes()
        frame_rate = wav_audio.getframerate()
        waveform = np.frombuffer(wav_audio.readframes(n_frames), dtype=np.int16)
        time = np.linspace(0, n_frames / frame_rate, num=n_frames)
        fig = Figure(figsize=(10, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, waveform)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Waveform Graph")
        canvas = FigureCanvasTkAgg(fig)
        canvas.get_tk_widget().place(relx=0.1, rely=0.3)
        canvas.draw()