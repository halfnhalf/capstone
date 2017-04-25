from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.screen_manager = self.audiometer.root

        layout = FloatLayout()
        go_to_demo_button = Button(text="Home", font_size=40, size_hint=(.25, .5),background_color = (1,.9,0,1),pos = (60,120))

        go_to_hearing_button = Button(text="Take Hearing Test", font_size = 25, size_hint=(.25, .5), background_color = (1,.9,0,1),pos = (300, 120))
        #go_to_results_button = Button(text="results", font_size=40)
        go_to_testresults_button = Button(text="Test Results", font_size=30, size_hint=(.25, .5), background_color = (1,.9,0,1),pos = (540,120))

        go_to_demo_button.bind(on_press=self.go_to_demo)
        go_to_hearing_button.bind(on_press=self.go_to_hearing)
        #go_to_results_button.bind(on_press=self.go_to_results)
        go_to_testresults_button.bind(on_press=self.go_to_testresults)

        layout.add_widget(go_to_demo_button)
        layout.add_widget(go_to_hearing_button)
        #layout.add_widget(go_to_results_button)
        layout.add_widget(go_to_testresults_button)

        self.add_widget(layout)

    def go_to_demo(self, instance):
        self.screen_manager.current = 'demo'

    def go_to_hearing(self, instance):
        self.screen_manager.current = 'hearing'

    #def go_to_results(self, instance):
     #   self.screen_manager.current = 'results'

    def go_to_testresults(self, instance):
        self.screen_manager.current = 'testresults'    