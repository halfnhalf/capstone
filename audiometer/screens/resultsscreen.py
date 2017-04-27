import json
import glob
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from operator import itemgetter, attrgetter, methodcaller
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        #self.layout = PageLayout(Page = 2)
        self.screen_manager = self.audiometer.root
        self.layout = FloatLayout()
        test_button = Button(text="Home", background_normal = "images/button.png", background_color = (0.9,0.9,0,1),color = (0,0,0,1),size_hint = (0.2,0.1), pos = (320,20), font_size = 20)
        test_button.bind(on_release=self.go_to_home)
        legend = Label(text = '[size=20][color=026cff]X[/size][/color] is Left ear\n[size=20][color=ff0217]O[/size][/color] is Right ear '
            , pos = (-340,-210), markup = True)
        self.loss = None
        self.air_picture = None
        self.bone_picture = None
        self.layout.add_widget(legend)
        self.layout.add_widget(test_button)
        self.add_widget(self.layout)

    def result_button_pressed(self, filename):
        #closes all previous widgets in order to display new widgets
        if self.air_picture is not None and self.bone_picture is not None:
            plt.close('all')
            self.layout.remove_widget(self.air_picture)
            self.layout.remove_widget(self.bone_picture)

        if self.loss is not None:
            self.layout.remove_widget(self.loss)

        self.filename = filename
        try:
            with open(os.path.join(os.path.dirname(__file__),'../../data/' + self.filename)) as json_data:
                results = json.load(json_data)

            #sets both ear axes for air
            check = None
            check2 = None
            hearingloss = 'empty'
            air_left_x = results['frequencies']
            air_left_y = results['air']['Left Ear']['decibels']
            air_right_x = results['frequencies']
            air_right_y = results['air']['Right Ear']['decibels']

            # this checks to see if it is running the full hearing test or quickstart
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

            #determines the hearing loss in air
            for i,b in zip(air_left_y,air_right_y):
                if i <=29 or b <=29:
                    if hearingloss == 'Moderate' or hearingloss == 'Severe' or hearingloss == 'Mild':
                        hearingloss = hearingloss
                    else:
                        hearingloss = 'No'
                        color_code = 1
                if 30 <= i <= 50 or 30 <= b <= 50:
                    if hearingloss == 'Moderate' or hearingloss == 'Severe':
                        hearingloss = hearingloss
                    else:
                        hearingloss = 'Mild'
                        color_code = 2
                if 51 <= i <= 69 or 51 <= b <= 69:
                    if hearingloss == 'Severe':
                        hearingloss = hearingloss
                    else:
                        hearingloss = "Moderate"
                        color_code = 3
                if 70 <= i or 70 <= b:
                        hearingloss = "Severe"
                        color_code = 4

            #sets both ear axes for bone
            bone_left_x = results['frequencies']
            bone_left_y = results['bone']['Left Ear']['decibels']
            bone_right_x = results['frequencies']
            bone_right_y = results['bone']['Right Ear']['decibels']

            #checks if quick start or full test for bone
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

            #determines the hearing loss in bone which will override air if need be
            for i,b in zip(bone_left_y,bone_right_y):
                if i <=29 or b <=29:
                    if hearingloss == 'Moderate' or hearingloss == 'Severe' or hearingloss == 'Mild':
                        hearingloss = hearingloss
                    else:
                        hearingloss = 'No'
                        color_code = 1
                if 30 <= i <= 50 or 30 <= b <= 50:
                    if hearingloss == 'Moderate' or hearingloss == 'Severe':
                        hearingloss = hearingloss
                    else:
                        hearingloss = 'Mild'
                        color_code = 2
                if 51 <= i <= 69 or 51 <= b <= 69:
                    if hearingloss == 'Severe':
                        hearingloss = hearingloss
                    else:
                        hearingloss = "Moderate"
                        color_code = 3
                if 70 <= i or 70 <= b:
                        hearingloss = "Severe"
                        color_code = 4

            #prints hearing loss text with colors
            if color_code == 1:
                self.loss = Label(text = "You Have [color=05fa22]%s[/color] Hearing Loss" % hearingloss, font_size = 30, pos = (10,-100), markup = True)
            if color_code == 2:
                self.loss = Label(text = "You Have [color=efff02]%s[/color] Hearing Loss" % hearingloss, font_size = 30, pos = (10,-100), markup = True)
            if color_code == 3:
                self.loss = Label(text = "You Have [color=ff9202]%s[/color] Hearing Loss" % hearingloss, font_size = 30, pos = (10,-100), markup = True)
            if color_code == 4:
                self.loss = Label(text = "You Have [color=ff3333]%s[/color] Hearing Loss" % hearingloss, font_size = 30, pos = (10,-100), markup = True)
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

            self.layout.add_widget(self.loss)
            self.layout.add_widget(self.air_picture)
            self.air_picture.reload()
            self.layout.add_widget(self.bone_picture)
            self.bone_picture.reload()

        except Exception as e:
            print str(e)

    def go_to_home(self, instance):
        self.screen_manager.current = 'home'


