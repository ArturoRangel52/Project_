#This program is taken from the L26 Lecture Slides

from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def select_file():
    filetypes = (('Wav files', '*.wav'), ('Mp3 files', '*.mp3'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Open File', initialdir='/', filetypes=filetypes)
    return filename

#open button
open_button = ttk.Button(root, text='Open File', command=select_file)
open_button.pack(expand=True)

src = "pt.mp3"
dst = "pt.wav"

sound = AudioSegment.from_mp3()
sound.export(dst, format="wav")

raw_audio = AudioSegment.from_file("pt.wav", format="wav")
channel_count = raw_audio.channels
mono_wav = raw_audio.set_channels(1)
mono_wav.export("pt_mono.wav", format="wav")
mono_wav_audio = AudioSegment.from_file("pt_mono.wav", format="wav")

sample_rate, data = wavfile.read(mono_wav_audio)
spectrum, freqs= plt.specgram(data, Fs=sample_rate)

#prints var outputs
def debugg(fstring): #debug variable values
    print(fstring)
    pass

def find_target_frequency(freqs): #find a mid-range frequency
    for x in freqs:
        if x > 1000:
            break
    return x

def frequency_check():#choose a frequency to check
    debugg(f'freqs {freqs[:10]}]')
    target_frequency = find_target_frequency(freqs)
    debugg(f'target_frequency {target_frequency}')
    index_of_frequency = np.where(freqs == target_frequency)[0][0] #find index of target_frequency
    debugg(f'index_of_frequency {index_of_frequency}')
    # find a sound data for a particular frequency

    data_for_frequency = spectrum[index_of_frequency]
    debugg(f'data_for_frequency {data_for_frequency[:10]}')
    #change a digital signal for values in decibels

    data_in_db_fun = 10 * np.log10(data_for_frequency) #use natural logarithm to get more audio-natural output
    return data_in_db_fun

data_in_db = frequency_check()
plt.figure()
#plot reverb time on grid

plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel('Time (s)')
plt.ylabel('Power (dB)')
#create plot and label

#find index of a max value
index_of_max = np.argmax(data_in_db)
#for computation and marking plot
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')

#slice array from a max value
sliced_array = data_in_db[index_of_max:]
#determine 5db less of max value
value_of_max_less_5 = value_of_max - 5

#find a nearest value
def find_nearest_value(array, value): #pass in sliced array list and value less 5db
    array = np.asarray(array)
    debugg(f'array {array[:10]}')
    idx = (np.abs(array - value)).argmin() #convert input into array
    debugg(f'idx {idx}')
    debugg(f'array[idx] {array[idx]}')
    return array[idx]

#determine absolute value and subtract less 5 db value
value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo') #plot values

#slice array from a max -5db
value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25) #determine -25db down
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro') #mark point on plot
rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0] #compute RT20

#extrapolate rt20 to rt60
rt60 = 3 * rt20 #extrapolate to RT60

#optional set limits on plot
#plt.xlim(0, ((round(abs(rt60), 2)) * 1.5)
plt.grid() #show grid
plt.show() #show plots

print(f'The RT60 reverb time is {round(abs(rt60), 2)} seconds')