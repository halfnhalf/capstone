import json
from math import sin
from kivy.uix.screenmanager import Screen
from kivy.garden.graph import Graph, MeshLinePlot, SmoothLinePlot
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.audiometer = kwargs['audiometer']
        self.audio_controller = self.audiometer.audio_controller
        self.screen_manager = self.audiometer.root
        self.layout = BoxLayout()
        graph_theme = {'background_color':'f8f8f2'}
        graph = Graph(xlabel='Frequency', ylabel='Decibel', x_ticks_minor=4,
			x_ticks_major=1000, y_ticks_major=10,
			y_grid_label=True, x_grid_label=True, padding=5,
			x_grid=True, y_grid=True, xmin=0, xmax=8000, ymin=-110, ymax=10
            )
        plot = MeshLinePlot(color=[1,0,0,1])
        plot.points = [(x, sin(x / 10.) ) for x in range(0, 101)]
        graph.add_plot(plot)
        #runTouchApp(graph)
        self.add_widget(graph)
        self.add_widget(self.layout)
       

#with open('/Users/jamesle/Documents/capstone/data/test.json') as json_data:
#   		results = json.load(json_data)
# 
#print "Frequencies: ", results['Left Ear'][0]['Frequencies']
#print "Decibels ", results['Right Ear'][0]['decibels']

	

	
