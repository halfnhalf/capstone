from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.label import Label


class InstructionScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.layout = FloatLayout(size_hint=(.5, .5),pos = (200,400))
        with open("Instruction.txt") as file:
            contents = file.read()
        print contents
        l = Label(text = contents)

        
        back= Button(text = 'Back',size_hint=(.2, .1),font_size = 20,pos = (240,100))
        back.bind(on_press=self.back)
        start= Button(text = 'Next',size_hint=(.2, .1),font_size = 20,pos = (400,100))
        start.bind(on_press=self.start)


        self.add_widget(back)
        self.add_widget(start)
        self.add_widget(l)
        self.add_widget(self.layout)

    def back(self, instance):
        self.screen_manager.current = 'demo'

    def start(self, instance):
        self.screen_manager.current = 'hearing'