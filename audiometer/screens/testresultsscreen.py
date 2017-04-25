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
        results_1_button = Button(text="result 1", size_hint = (0.35,0.35),background_color = (1,1,0,0.8), font_size = 20, pos = (110,280))
        results_2_button = Button(text="result 2", size_hint = (0.35,0.35), background_color = (0,1,0,0.8), font_size = 20, pos = (420,280))
        results_1_button.bind(on_press=self.go_to_results_1)
        results_2_button.bind(on_press=self.go_to_results_2)

        back= Button(text = 'Back',size_hint=(.2, .1),font_size = 20,background_color = (1,0,0,1),pos = (230,100))
        back.bind(on_press=self.back)

        home = Button(text="Home", font_size = 20, size_hint=(.2, .1),background_color = (1,0,0,1),pos = (410,100))
        home.bind(on_press=self.home)

        self.add_widget(results_1_button)
        self.add_widget(results_2_button)
        self.add_widget(self.layout)
        self.add_widget(back)
        self.add_widget(home)



    def go_to_results_1(self, instance):
        self.audiometer.root.get_screen('results').result_button_pressed('test2.json')

    def go_to_results_2(self, instance):
        self.audiometer.root.get_screen('results').result_button_pressed('current_audiogram.json')

    def back(self, instance):
        self.screen_manager.current = 'menu'

    def home(self, instance):
        self.screen_manager.current = 'demo'
