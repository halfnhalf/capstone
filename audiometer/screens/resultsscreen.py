import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from kivy.uix.button import Button
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image



class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        #self.layout = PageLayout(Page = 2)
        self.screen_manager = self.audiometer.root
        self.layout = FloatLayout(size=(800, 480))
        test_button = Button(text="Home", background_normal = "images/button.png", background_color = (0.9,0.9,0,1),color = (0,0,0,1),size_hint = (0.2,0.1), pos = (320,20), font_size = 20)
        test_button.bind(on_release=self.go_to_home)

        self.air_picture = None
        self.bone_picture = None
        self.layout.add_widget(test_button)
        self.add_widget(self.layout)
        #self.result_button_pressed(self.filename)

    def result_button_pressed(self, filename):
        if self.air_picture is not None and self.bone_picture is not None:
            plt.close('all')
            self.layout.remove_widget(self.air_picture)
            self.layout.remove_widget(self.bone_picture)

        self.filename = filename
        try:
            with open(os.path.join(os.path.dirname(__file__),'../../data/' + self.filename)) as json_data:
                results = json.load(json_data)


            #sets both ear axes for air
            check = None
            check2 = None
            air_left_x = results['frequencies']
            air_left_y = results['air']['Left Ear']['decibels']
            air_right_x = results['frequencies']
            air_right_y = results['air']['Right Ear']['decibels']
            if air_left_x == [1000]:
                air_left_x = [250,500,1000,2000,4000,8000]
                air_right_x = [250,500,1000,2000,4000,8000]
                check = air_left_y[0]
                check2 = air_right_y[0]
                air_left_y = [] 
                air_right_y = []
                for i in air_left_x:
                    if i != 1000:
                        air_left_y.insert(i,-20)
                        air_right_y.insert(i,-20)
                    else:
                        air_left_y.insert(i,check)
                        air_right_y.insert(i,check2)

            #sets both ear axes for bone
            bone_left_x = results['frequencies']
            bone_left_y = results['bone']['Left Ear']['decibels']
            bone_right_x = results['frequencies']
            bone_right_y = results['bone']['Right Ear']['decibels']
            if bone_left_x == [1000]:
                bone_left_x = [250,500,1000,2000,4000,8000]
                bone_right_x = [250,500,1000,2000,4000,8000]
                check = bone_left_y[0]
                check2 = bone_right_y[0]
                bone_left_y = [] 
                bone_right_y = []
                for i in bone_left_x:
                    if i != 1000:
                        bone_left_y.insert(i,-20)
                        bone_right_y.insert(i,-20)
                    else:
                        bone_left_y.insert(i,check)
                        bone_right_y.insert(i,check2)

            ##plots air conduction
            air = plt.figure()
            air_graph = air.add_subplot(111)
            plt.title('Air')
            plt.xlabel('Frequency(Hz)')
            plt.ylabel('decibel(dB)')
            plt.ylim((120,-10))
            mpl.rcParams.update({'font.size': 14})
            air_graph.grid(which = "both")
            x_plot = range(len(air_left_y))
            x2_plot = range(len(air_right_y))
            # major_ticks = np.arange(-10, 121, 10)                                              
            # minor_ticks = np.arange(-10, 121, 5)
            # air_graph.set_yticks(major_ticks)
            # air_graph.set_yticks(minor_ticks, minor=True)
            major_ticks = np.arange(0, 121, 20)                                              
            minor_ticks = np.arange(-10, 121, 5)
            air_graph.set_yticks(major_ticks)
            air_graph.set_yticks(minor_ticks, minor=True)
            if check != None:
                air_graph.plot(x_plot ,air_left_y, 'bx', markersize = 12)
                air_graph.plot(x2_plot,air_right_y, 'ro', markersize =12)
            else:
                air_graph.plot(x_plot ,air_left_y, 'bx-', markersize = 12)
                air_graph.plot(x2_plot,air_right_y, 'ro-', markersize =12)
            plt.xticks(x_plot, air_left_x)
            plt.savefig('Air Conduction.png')
            self.air_picture = Image(source='Air Conduction.png', size_hint = (0.48,1), pos = (10, 80))

            ## plots bone conduction
            bone = plt.figure()
            bone_graph = bone.add_subplot(111)
            plt.title('Bone')
            plt.xlabel('Frequency(Hz)')
            plt.ylabel('decibel(dB)')
            mpl.rcParams.update({'font.size': 14})
            plt.grid(which = "both")
            major_ticks = np.arange(0, 121, 20)                                              
            minor_ticks = np.arange(-10, 121, 5)
            bone_graph.set_yticks(major_ticks)
            bone_graph.set_yticks(minor_ticks, minor=True)
            plt.ylim((120,-10))
            x3_plot = range(len(bone_left_y))
            x4_plot = range(len(bone_right_y))
            if check != None:
                bone_graph.plot(x3_plot ,bone_left_y, 'bx', markersize = 12)
                bone_graph.plot(x4_plot,bone_right_y, 'ro', markersize =12)
            else:
                bone_graph.plot(x3_plot ,bone_left_y, 'bx-', markersize = 12)
                bone_graph.plot(x4_plot,bone_right_y, 'ro-', markersize =12)
            plt.xticks(x3_plot, bone_left_x)
            plt.savefig('Bone Conduction.png')
            self.bone_picture = Image(source='Bone Conduction.png', size_hint = (0.48,1), pos = (405,80))

            self.layout.add_widget(self.air_picture)
            self.air_picture.reload()
            self.layout.add_widget(self.bone_picture)
            self.bone_picture.reload()

        except Exception as e:
            print str(e)

    def go_to_home(self, instance):
        self.screen_manager.current = 'home'