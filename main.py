from kivy.config import Config

Config.set('graphics', 'height', '480')
Config.set('graphics', 'width', '800')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from audiometer.screens import MenuScreen, HomeScreen, HearingScreen, ResultsScreen,TestResultsScreen, InstructionScreen
from audiometer.audio.audiocontroller import AudioController

class Audiometer(App):
    # these variables are static
    # our app shouldn't have more than 1 of each at a time
    root = ScreenManager()
    audio_controller = AudioController()

    def build(self):
        Audiometer.root.add_widget(HomeScreen(
            name='home',
            audiometer=Audiometer))
        Audiometer.root.add_widget(MenuScreen(
            name='menu',
            audiometer=Audiometer))
        Audiometer.root.add_widget(HearingScreen(
            name='hearing',
            audiometer=Audiometer))
        Audiometer.root.add_widget(ResultsScreen(
            name='results',
            filename = 'current_audiogram.json',
            audiometer=Audiometer))
        Audiometer.root.add_widget(TestResultsScreen(
            name='testresults',
            filename = 'test2.json',  
            audiometer=Audiometer))
        Audiometer.root.add_widget(InstructionScreen(
            name='instruction',
            audiometer=Audiometer))
        return Audiometer.root

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        if Audiometer.test:
            Audiometer.test.stop_thread()


if __name__ == '__main__':
    Audiometer().run()
