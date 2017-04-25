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
from kivy.uix.image import Image

import threading

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        
        
        self.rams = Image(source='./images/vcu.png', size_hint = (0.25,0.25),pos = (230,330))
        

        layout = FloatLayout(size = (800,480))

        Window.clearcolor = (0,0,0,1)

        vcu = Label(text = 'VCU',color = (1,.8,0,1), font_size = 60,pos = (60,150))
        debug = Button(text = 'Debug', size_hint=(.15, .15),background_color = (1,0,0,0.8),font_size = 20,pos = (20,20))
        go_to_hearing_button= Button(text = 'Take your test!',size_hint=(.5, .2),background_color = (0,1,0,2),font_size = 20,pos = (205,210))
        go_to_hearing_button.bind(on_press=self.go_to_instruction)

        #background_normal='images/button_normal.png'
        result1= Button(text = 'Result 1',size_hint=(.15, .05),background_color = (0,1,0,1),font_size = 15,pos = (340,140))
        result1.bind(on_press=self.go_to_results_1)

        result2= Button(text = 'Result 2',size_hint=(.15, .05),background_color = (0,1,0,1),font_size = 15,pos = (340,100))
        result2.bind(on_press=self.go_to_results_2)


        go_to_menu_button = Button(text="Menu", background_color = (1,0,0,0.8), font_size = 20, size_hint=(.15, .15),pos = (660,20))
        go_to_menu_button.bind(on_press=self.go_to_menu)


        layout.add_widget(go_to_menu_button)
        layout.add_widget(go_to_hearing_button)
        layout.add_widget(debug)
        layout.add_widget(vcu)
        layout.add_widget(result1)
        layout.add_widget(result2)
        self.add_widget(layout)
        self.add_widget(self.rams)
        

    def go_to_menu(self, instance):
        self.screen_manager.current = 'menu'

    def go_to_instruction(self, instance):
        self.screen_manager.current = 'instruction'

    def go_to_results_1(self, instance): #<--------------------
        self.audiometer.root.get_screen('results').result_button_pressed('test.json') 
        self.screen_manager.current = 'results'

    def go_to_results_2(self, instance): #<--------------------
        self.audiometer.root.get_screen('results').result_button_pressed('test2.json')
        self.screen_manager.current = 'results'
