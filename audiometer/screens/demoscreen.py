from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class DemoScreen(Screen):
    def __init__(self, **kwargs):
        super(DemoScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root

        layout = GridLayout(cols=2)
        slider = Slider(min=110, max=880, value=440)
        toggle_sound_button = Button(text="toggle sound", font_size = 40)
        mute_left_channel_button = Button(text="Mute Left Channel", font_size = 40)
        go_to_menu_button = Button(text="Menu", font_size = 40)

        slider.bind(value=self.audio_controller.update_freq)
        toggle_sound_button.bind(on_press=self.audio_controller.toggle_sound)
        go_to_menu_button.bind(on_press=self.go_to_menu)

        layout.add_widget(slider)
        layout.add_widget(toggle_sound_button)
        layout.add_widget(mute_left_channel_button)
        layout.add_widget(go_to_menu_button)

        self.add_widget(layout)

    def go_to_menu(self, instance):
        self.screen_manager.current = 'menu'
