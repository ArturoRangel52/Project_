import tkinter as tk

class View:
    def __init__(self, model): #variables initialized and defined
        self.filename = None
        self.message_label = None
        self.open_button = None
        self.label = None
        self.root = tk.Tk()
        self.root.title('Test')
        self.root.resizable(False, False)
        self.root.geometry('1200x700')

    def set_model(self, model):
        self.model = model

    def mainloop(self):
        tk.mainloop()