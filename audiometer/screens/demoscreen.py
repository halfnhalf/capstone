from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from audiometer.hearing.hearingtest import HearingTest
import threading

class DemoScreen(Screen):
    def __init__(self, **kwargs):
        super(DemoScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root

        layout = FloatLayout()
        debug = Button(text = 'Debug',size_hint=(.15, .15),font_size = 20,pos = (20,20))
        go_to_hearing_button= Button(text = 'Take your test!',size_hint=(.5, .2),font_size = 20,pos = (200,250))
        go_to_hearing_button.bind(on_press=self.go_to_instruction)
        go_to_menu_button = Button(text="Menu", font_size = 20, size_hint=(.15, .15),pos = (660,20))

        
        go_to_menu_button.bind(on_press=self.go_to_menu)

        #layout.add_widget(slider)
        #layout.add_widget(play_sound_button)
        #layout.add_widget(stop_sound_button)
        layout.add_widget(go_to_menu_button)
        self.add_widget(go_to_hearing_button)
        self.add_widget(layout)
        self.add_widget(debug)

    def go_to_menu(self, instance):
        self.screen_manager.current = 'menu'

    def go_to_instruction(self, instance):
        self.screen_manager.current = 'instruction'
