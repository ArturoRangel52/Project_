import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class View:
    def __init__(self, model):
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
        pass
    
    def create_widgets(self):
        #File Select
        self.slabel = ttk.Label(text="Enter Audio Sample: ")
        self.slabel.grid(row=1, column=0)

        #open button
        self.open_button = ttk.Button(text='Open File', command=self.select_file)
        self.open_button.grid(row=1, column=1, padx=10)

        #message
        self.message_label = ttk.Label(text='', foreground='red')
        self.message_label.grid(row=2, column=1, sticky=tk.W)


        #Mat Plot 
        self.plabel = ttk.Label(text="Sound Graph")
        self.plabel.grid(row=3, column=0)
        #Button to plot graph
        self.plot_button = ttk.Button(master = root, text="Plot Graph", command = self.model)
        self.plot_button.grid(row = 4, column = 0)


    def select_file(self):

        filetypes = (('Wav files', '*.wav'), ('Mp3 files', '*.mp3'), ('All files', '*.*'))
        filename = fd.askopenfilename(title='Open File', initialdir='/', filetypes=filetypes)

        #tkinter.messagebox - Tkinter message prompts
        if(filename == ""):
            showinfo(title='Please Select a File', message="No File Selected.")
        else:    
            showinfo(title='Selected File', message=filename)


#create the root window
root = tk.Tk()
root.title('Selected Audio')
root.resizable(False, False)
root.geometry('1200x600')

window = View(root)
root.mainloop()

