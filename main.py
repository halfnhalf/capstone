#from kivy.config import Config
#Config.set('graphics', 'maxfps', '60')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from audiometer import MenuScreen, DemoScreen


class Audiometer(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(DemoScreen(name='demo'))
        self.sm.add_widget(MenuScreen(name='menu'))
        return self.sm


if __name__ == '__main__':
    Audiometer().run()
