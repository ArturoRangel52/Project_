from model import Model
from view import View
from controller import Controller

if __name__ == '__main__': #starts program
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    view.mainloop()
