from audiostream import get_output
from audiostream.sources.wave import SineSource
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

CHANNELS = 2
BUFSIZE = 2048
INCSIZE = 512

class DemoScreen(Screen):
    sound_is_playing = False

    def __init__(self, **kwargs):
        super(DemoScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=2)
        slider = Slider(min=110, max=880, value=440)
        button = Button(text="toggle sound", font_size = 14)

        slider.bind(value=self.update_freq)
        button.bind(on_press=self.play_freq)


        layout.add_widget(slider)
        layout.add_widget(button)

        self.add_widget(layout)

    def update_freq(self, slider, value):
        #value = int(value / 50) * 50
        if value != self.source.frequency:
            self.source.frequency = value
    
    def play_freq(self, instance):
        if not self.sound_is_playing:
            stream = get_output(channels=CHANNELS, buffersize=BUFSIZE, rate=22050)
            self.source = SineSource(stream, 440)
            self.source.start()
        else:
            self.source.stop()

        self.sound_is_playing = not self.sound_is_playing
