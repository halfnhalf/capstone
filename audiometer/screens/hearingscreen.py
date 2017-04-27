from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from audiometer.hearing.hearingtest import HearingTest
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock, mainthread
import threading
from kivy.uix.image import Image

class HearingScreen(Screen):
    def __init__(self, **kwargs):
        super(HearingScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.audiometer.test = HearingTest(audiometer=self.audiometer)

        self.layout = FloatLayout()
        self.heard_button = Button(text="I hear it!", color = (0,0,0,1),background_normal = "images/button.png",font_size=50,background_color = (0.9,0.9,0,1), size_hint=(.4, .4),pos = (240,230))
        self.start_button = Button(text="Start Test!", font_size=20, background_color = (0,1,0,1), size_hint=(.2, .1),pos = (320,100))
        back= Button(text = 'Instruction',size_hint=(.2, .1),font_size = 20,background_color = (1,0,0,1),pos = (140,100))
        back.bind(on_release=self.back)

        home = Button(text="Home", font_size = 20, size_hint=(.2, .1),background_color = (1,0,0,1),pos = (500,100))
        home.bind(on_release=self.home)

        self.vcurams = Image(source='./images/vcurams.png', size_hint = (0.2,0.2),pos = (630,-5))

        #self.ece = Image(source='./images/ece.png', size_hint = (0.25,0.25),pos = (580,5))


        self.heard_button.bind(on_release=self.on_heard_press)
        self.start_button.bind(on_release=self.on_start_press)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.heard_button)
        self.layout.add_widget(back)
        self.layout.add_widget(home)
        self.add_widget(self.layout)
        self.add_widget(self.vcurams)  
        #self.add_widget(self.ece)

    def on_start_press(self, instance):
        #Start thread with test
        self.audiometer.test.stop.clear()
        threading.Thread(target=self.test_thread).start()
        self.start_button.funbind('on_press', self.on_start_press)
        self.start_button.fbind('on_press', self.on_stop_press)
        self.start_button.text = "Stop Test!"

    def on_stop_press(self, instance):
        self.audiometer.test.stop_thread()
        self.start_button.funbind('on_press', self.on_stop_press)
        self.start_button.fbind('on_press', self.on_start_press)
        self.start_button.text = "Start Test!"

    def on_heard_press(self, instance):
        self.audiometer.test.button_press()

    def test_thread(self):
        #Do test
        self.audiometer.test.start_test_sequence()
        #Leave page
        self.thread_ended_go_to_results()

    @mainthread
    def thread_ended_go_to_results(self):
        self.on_stop_press(None)
        self.audiometer.test.stop.clear()
        self.audiometer.root.get_screen('results').result_button_pressed('current_audiogram.json')
        self.screen_manager.current = 'results'


    def back(self, instance):
        self.screen_manager.current = 'instruction'
        self.screen_manager.transition.direction='right'

    def home(self, instance):
        self.screen_manager.current = 'home'
        self.screen_manager.transition.direction='right'

