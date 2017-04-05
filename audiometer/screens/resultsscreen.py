from kivy.uix.screenmanager import Screen

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
