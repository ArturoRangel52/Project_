Welcome to the Scientific Python Interactive Data Acoustic Modeling (SPIDAM) Project!

This project sets out to enable users to import, visualize, analyze, and model audio samples using calculations and data visualization tools.

Naturally, the featured program will conduct the processes behind the scenes while the user is greeted by a GUI to effortlessly produce results.

The prompt given from which this project was built off of was the problem of voice intelligibility in enclosed spaces, where factors such as size and padding may produce long reverberation times, likely to disrupt hearing and speaking.

In short, longer reverb decay impairs voice intelligibility, making comprehension and understanding difficult for listeners.

The program identifies the frequency ranges with the longest reverb times to create a solution that implements appropriate acoustic treatment by dampening the aforementioned frequency ranges. Primarily, the goal was to create a short and consistent reverb time (fewer than half a second) over the audible frequency spectrum (20 hertz to 20 kilohertz)

The program was tested with an audio sample of a clap recorded by a device 3 meters from the source and in an enclosed space with a minimum of RT60 greater than 1 second (reverb time). 

Libraries and packages utilized to analyze the audio will be listed in the requirement.txt file. 

The program display a graphical user interface and allow the user to load a data file from various locations, clean the audio data to be properly analyzed, produce a summary of statistics and measures within the audio sample, provide visualizations of the data, and reduce the RT60 to a maximum voice intelligibility of 0.5 seconds. 

Start the program by running it in your desired software and use the buttons to explore the desired audio file.

The team hopes it functions as well as it is intended to!