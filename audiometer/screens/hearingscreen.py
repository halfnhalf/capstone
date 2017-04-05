from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.gridlayout import GridLayout

class HearingScreen(Screen):
    def __init__(self, **kwargs):
        super(HearingScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root


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
