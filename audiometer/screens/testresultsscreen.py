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
        results_1_button = Button(text="results1", size_hint = (0.25,0.25), pos = (400,400))
        results_2_button = Button(text="results2", size_hint = (0.25,0.25))
        results_1_button.bind(on_press=self.go_to_results_1)
        results_2_button.bind(on_press=self.go_to_results_2)
        self.add_widget(results_1_button)
        self.add_widget(results_2_button)
        self.add_widget(self.layout)


    def go_to_results_1(self, instance):
        self.audiometer.root.get_screen('results').result_button_pressed('test2.json')

    def go_to_results_2(self, instance):
        self.audiometer.root.get_screen('results').result_button_pressed('current_audiogram.json')