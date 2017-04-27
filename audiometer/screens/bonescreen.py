from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.base import runTouchApp

class BoneScreen(Screen):
    def __init__(self, **kwargs):
        super(BoneScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root

        layout = FloatLayout(size = (800,480))
        self.play_button = Button(text="Toggle Sound!", font_size=20, background_color = (0,1,0,1))
        self.play_button.bind(on_release = self.play_sound)

        home = Button(text="Home", font_size = 20, size_hint=(.2, .1),background_color = (1,0,0,1),pos = (-260,190))
        home.bind(on_press=self.home)

        layout.add_widget(self.play_button)
        layout.add_widget(home)
        self.add_widget(layout)

    def play_sound(self, instance):
        self.audio_controller.play_sound(frequencies=[(1000, 0.5),(1000, 0.5),(1000,0),(1000,0)])  
        self.change_to_stop()

    def stop_sound(self,instance):
        if self.audio_controller.sound_is_playing:
            self.audio_controller.stop_sound()
        self.change_to_start()

    def change_to_start(self):
        self.play_button.unbind(on_release=self.stop_sound)
        self.play_button.bind(on_release=self.play_sound)

    def change_to_stop(self):
        self.play_button.unbind(on_release=self.play_sound)
        self.play_button.bind(on_release=self.stop_sound)

    def home(self):
        self.screen_manager.current = 'home'

    def on_leave(self):
        if self.audio_controller.sound_is_playing:
            self.audio_controller.stop_sound()

        