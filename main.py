#from kivy.config import Config
#Config.set('graphics', 'maxfps', '30')

from audiostream import get_output
from audiostream.sources.wave import SineSource

CHANNELS = 2
BUFSIZE = 2048
INCSIZE = 512

from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class MenuScreen(Screen):
    pass

class DemoScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(DemoScreen(name='demo'))
sm.add_widget(MenuScreen(name='menu'))

class AudioApp(App):
    def build(self):
        self.stream = get_output(channels=CHANNELS, buffersize=BUFSIZE, rate=22050)
        self.slider = Slider(min=110, max=880, value=440)
        self.slider.bind(value=self.update_freq)

        self.button = Button(text="Left", font_size = 14)

        self.source = SineSource(self.stream, 440)
        self.source.start()

        return self.slider

    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if value != self.source.frequency:
            self.source.frequency = value


if __name__ == '__main__':
    AudioApp().run()
