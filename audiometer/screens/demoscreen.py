from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from audiometer.hearing.hearingtest import HearingTest
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
import threading

class DemoScreen(Screen):
    def __init__(self, **kwargs):
        super(DemoScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        
        
        

        layout = FloatLayout(size = (800,480))

        Window.clearcolor = (0,0,0,1)

        vcu = Label(text = 'VCU',color = (1,1,0,1), font_size = 60,pos = (10,180))
        debug = Button(text = 'Debug', size_hint=(.15, .15),background_color = (1,0,0,0.8),font_size = 20,pos = (20,20))
        go_to_hearing_button= Button(text = 'Take your test!',size_hint=(.5, .2),background_color = (0,1,0,2),font_size = 20,pos = (200,250))
        go_to_hearing_button.bind(on_press=self.go_to_instruction)
        #go_to_hearing_button= InstructionGroup()
        #go_to_hearing_button.add(c)

        go_to_menu_button = Button(text="Menu", background_color = (1,0,0,0.8), font_size = 20, size_hint=(.15, .15),pos = (660,20))
        go_to_menu_button.bind(on_press=self.go_to_menu)

        #layout.add_widget(slider)
        #layout.add_widget(play_sound_button)
        #layout.add_widget(stop_sound_button)
        layout.add_widget(go_to_menu_button)
        layout.add_widget(go_to_hearing_button)
        layout.add_widget(debug)
        layout.add_widget(vcu)
        self.add_widget(layout)
       

    def go_to_menu(self, instance):
        self.screen_manager.current = 'menu'

    def go_to_instruction(self, instance):
        self.screen_manager.current = 'instruction'

