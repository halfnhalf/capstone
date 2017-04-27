from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.label import Label
from kivy.uix.image import Image



class InstructionScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.layout = FloatLayout(size_hint=(.5, .5),pos = (200,400))
        with open("Instruction.txt") as file:
            contents = file.read()
            #state = OptionProperty("None", options=["middle"])
        #print contents
        instructionlabel = Label(text = contents, font_size = 15,pos = (20,50))

        back= Button(text = 'Home', size_hint=(.2, .1),font_size = 20,background_color = (1,0,0,0.8), pos = (230,50))        
        back.bind(on_release=self.back)
        start= Button(text = 'Next',size_hint=(.2, .1),font_size = 20,background_color = (0,1,0,2), pos = (410,50))
        start.bind(on_release=self.start)


        self.add_widget(back)
        self.add_widget(start)
        self.add_widget(instructionlabel)
        self.add_widget(self.layout)

    def back(self, instance):
        self.screen_manager.transition.direction='right'
        self.screen_manager.current = 'home'

    def start(self, instance):
        self.screen_manager.transition.direction='left'
        self.screen_manager.current = 'hearing'
