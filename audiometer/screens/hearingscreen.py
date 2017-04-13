from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from audiometer.hearing.hearingtest import HearingTest
import threading

class HearingScreen(Screen):
    def __init__(self, **kwargs):
        super(HearingScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.audiometer.test = HearingTest(audiometer=self.audiometer)

        self.layout = BoxLayout(orientation='vertical')
        self.heard_button = Button(text="I hear it!", font_size=50)
        self.start_button = Button(text="Start Test!", font_size=50)
        self.heard_button.bind(on_press=self.on_heard_press)
        self.start_button.bind(on_press=self.on_start_press)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.heard_button)
        self.add_widget(self.layout)

    def on_start_press(self, instance):
        #Disable button
        instance.disabled = True
        #Start thread with test
        threading.Thread(target=self.test_thread).start()

    def on_heard_press(self, instance):
        self.audiometer.test.button_press()


    def test_thread(self):
        #Do test
        self.audiometer.test.start_test_sequence()
        #Leave page
        self.screen_manager.current = 'demo'




#dropdown = DropDown()
#for index in range(10):
#	btn = Button(text='Value %d' %index, size_hint_y=None, height = 44)
#	btn.bind(on_release = lambda btn: dropdown.select(btn.text))
#	dropdown.add_widget(btn)
#mainbutton = Button(text = 'hello', size_hint=(None, None))
#mainbutton.bind(on_release=dropdown.open)
#dropdown.bind(on_select =lambda instance, x: setattr(mainbutton, 'text', x))

#if __name__ == '__main__':
#runTouchApp(mainbutton)
