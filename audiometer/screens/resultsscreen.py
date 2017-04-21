import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
<<<<<<< HEAD
from kivy.uix.button import Button
=======
import os
>>>>>>> ed4b75caf85fc9c75324c48c7d194223e6ba4d32
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image



class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.layout = FloatLayout(size=(800, 480))
        test_button = Button(text="back", size_hint = (1,0.25), pos = (0,400), font_size = 20)
        test_button.bind(on_press=self.go_to_menu)
        #opens json file, change directory
        with open(os.path.join(os.path.dirname(__file__),'../../data/test.json')) as json_data:
                results = json.load(json_data)

        #sets both ear axes for air
        air_left_x = results['air']['Left Ear'][0]['Frequencies']
        air_left_y = results['air']['Left Ear'][0]['decibels']
        air_right_x = results['air']['Right Ear'][0]['Frequencies']
        air_right_y = results['air']['Right Ear'][0]['decibels']

        #sets both ear axes for bone
        bone_left_x = results['bone']['Left Ear'][0]['Frequencies']
        bone_left_y = results['bone']['Left Ear'][0]['decibels']
        bone_right_x = results['bone']['Right Ear'][0]['Frequencies']
        bone_right_y = results['bone']['Right Ear'][0]['decibels']

        ##plots air conduction
        air = plt.figure()
        air_graph = air.add_subplot(111)
        plt.title('Air')
        plt.xlabel('Frequency(Hz)')
        plt.ylabel('decibel(dB)')
        plt.ylim((60,0))
        air_graph.plot(air_left_x,air_left_y, 'bx-', markersize = 12)
        air_graph.plot(air_right_x,air_right_y, 'ro-', markersize =12)
        plt.savefig('Air Conduction.png')
        air_picture = Image(source='Air Conduction.png', size_hint = (0.5,1))

        ## plots bone conduction
        bone = plt.figure()
        bone_graph = bone.add_subplot(111)
        plt.title('Bone')
        plt.xlabel('Frequency(Hz)')
        plt.ylabel('decibel(dB)')
        plt.ylim((60,0))
        bone_graph.plot(bone_left_x,bone_left_y, 'bx-', markersize = 12)
        bone_graph.plot(bone_right_x,bone_right_y, 'ro-', markersize =12)
        plt.savefig('Bone Conduction.png')
        bone_picture = Image(source='Bone Conduction.png', size_hint = (0.5,1), pos = (410,0))

        self.add_widget(air_picture)
        self.add_widget(bone_picture)
        self.add_widget(test_button)
        self.add_widget(self.layout)

    def go_to_menu(self, instance):
        self.screen_manager.current = 'menu'


	

	
