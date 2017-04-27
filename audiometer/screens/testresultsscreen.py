import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from kivy.uix.button import Button
import os
from kivy.uix.screenmanager import Screen
#from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


class TestResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(TestResultsScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.layout = GridLayout(cols=2)
        self.screen_manager = self.audiometer.root
        self.filename = kwargs['filename']
        result_button_color = (1,1,0,1)
        results_1_button = Button(text="result 1", size_hint = (0.35,0.07),color = (0,0,0,1),background_normal = "images/button.png", background_color = result_button_color, font_size = 20, pos = (260,390))
        results_2_button = Button(text="result 2", size_hint = (0.35,0.07),color = (0,0,0,1),background_normal = "images/button.png", background_color = result_button_color, font_size = 20, pos = (260,345))
        results_3_button = Button(text="result 3", size_hint = (0.35,0.07),color = (0,0,0,1),background_normal = "images/button.png", background_color = result_button_color, font_size = 20, pos = (260,300))
        results_4_button = Button(text="result 4", size_hint = (0.35,0.07),color = (0,0,0,1),background_normal = "images/button.png", background_color = result_button_color, font_size = 20, pos = (260,255))
        results_5_button = Button(text="result 5", size_hint = (0.35,0.07),color = (0,0,0,1),background_normal = "images/button.png", background_color = result_button_color, font_size = 20, pos = (260,210))





        results_1_button.bind(on_release=self.go_to_results_1)
        results_2_button.bind(on_release=self.go_to_results_2)
        results_3_button.bind(on_release=self.go_to_results_1)
        results_4_button.bind(on_release=self.go_to_results_1)
        results_5_button.bind(on_release=self.go_to_results_1)

        back= Button(text = 'Back',size_hint=(.2, .1),font_size = 20,background_color = (1,0,0,1),pos = (230,100))
        back.bind(on_release=self.back)

        home = Button(text="Home", font_size = 20, size_hint=(.2, .1),background_color = (1,0,0,1),pos = (410,100))
        home.bind(on_release=self.home)

        self.add_widget(results_1_button)
        self.add_widget(results_2_button)
        self.add_widget(results_3_button)
        self.add_widget(results_4_button)
        self.add_widget(results_5_button)
        self.add_widget(self.layout)
        self.add_widget(back)
        self.add_widget(home)



    def go_to_results_1(self, instance):
        self.audiometer.root.get_screen('results').result_button_pressed('test.json')
        self.screen_manager.current = 'results'

    def go_to_results_2(self, instance):
        self.audiometer.root.get_screen('results').result_button_pressed('test2.json')
        self.screen_manager.current = 'results'

    def back(self, instance):
        self.screen_manager.current = 'menu'
        self.screen_manager.transition.direction='right'

    def home(self, instance):
        self.screen_manager.current = 'home'
        self.screen_manager.transition.direction='right'

