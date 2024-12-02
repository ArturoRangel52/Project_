class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.root = self.view.root

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view