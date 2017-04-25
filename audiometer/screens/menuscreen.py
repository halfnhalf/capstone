from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.screen_manager = self.audiometer.root

        layout = GridLayout(cols=3)
        go_to_demo_button = Button(text="Home", font_size=40)

        go_to_hearing_button = Button(text="hearing", font_size = 40)
        go_to_results_button = Button(text="results", font_size=40)
        go_to_testresults_button = Button(text="testresults", font_size=40)

        go_to_demo_button.bind(on_press=self.go_to_demo)
        go_to_hearing_button.bind(on_press=self.go_to_hearing)
        go_to_results_button.bind(on_press=self.go_to_results)
        go_to_testresults_button.bind(on_press=self.go_to_testresults)

        layout.add_widget(go_to_demo_button)
        layout.add_widget(go_to_hearing_button)
        layout.add_widget(go_to_results_button)
        layout.add_widget(go_to_testresults_button)

        self.add_widget(layout)

    def go_to_demo(self, instance):
        self.screen_manager.current = 'demo'

    def go_to_hearing(self, instance):
        self.screen_manager.current = 'hearing'

    def go_to_results(self, instance):
        self.screen_manager.current = 'results'

    def go_to_testresults(self, instance):
        self.screen_manager.current = 'testresults'    