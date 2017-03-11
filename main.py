from kivy.config import Config
Config.set('graphics', 'height', '480')
Config.set('graphics', 'width', '800')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from audiometer.screens import MenuScreen, DemoScreen

class Audiometer(App):
    root = ScreenManager()

    def build(self):
        self.root = ScreenManager()
        self.root.add_widget(DemoScreen(name='demo'))
        self.root.add_widget(MenuScreen(name='menu'))
        return self.root


if __name__ == '__main__':
    Audiometer().run()
