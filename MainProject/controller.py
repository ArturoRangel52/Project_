



class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.root = self.view.root
        self.output_path = "cleaned.wav"
        self.setup_callbacks()

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def setup_callbacks(self):
        pass

    def process_audio(self, output_path):
        audio_data = self.model.read_audio(self.view.gfile)
