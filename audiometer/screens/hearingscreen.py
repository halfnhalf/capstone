from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from audiometer.hearing.hearingtest import HearingTest
from kivy.uix.floatlayout import FloatLayout
import threading

class HearingScreen(Screen):
    def __init__(self, **kwargs):
        super(HearingScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.audiometer.test = HearingTest(audiometer=self.audiometer)

        self.layout = FloatLayout()
        self.heard_button = Button(text="I hear it!", font_size=50,background_color = (1,1,0,1), size_hint=(.4, .4),pos = (410,250))
        self.start_button = Button(text="Start Test!", font_size=50, background_color = (0,1,0,1), size_hint=(.4, .4),pos = (70,250))
        back= Button(text = 'Back',size_hint=(.2, .1),font_size = 20,background_color = (1,0,0,1),pos = (230,100))
        back.bind(on_press=self.back)

        home = Button(text="Home", font_size = 20, size_hint=(.2, .1),background_color = (1,0,0,1),pos = (410,100))
        home.bind(on_press=self.home)

        self.heard_button.bind(on_press=self.on_heard_press)
        self.start_button.bind(on_press=self.on_start_press)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.heard_button)
        self.layout.add_widget(back)
        self.layout.add_widget(home)
        self.add_widget(self.layout)  

    def on_start_press(self, instance):
        #Start thread with test
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
        self.audiometer.test.stop.clear()
        #Leave page
        self.audiometer.root.get_screen('results').result_button_pressed('current_audiogram.json')
        self.screen_manager.current = 'results'

    def back(self, instance):
        self.screen_manager.current = 'instruction'

    def home(self, instance):
        self.screen_manager.current = 'home'

