from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty

__author__ = 'Nathan Johnston'

STATES = {'QLD': "Queensland", 'NSW': "New South Wales", 'VIC': "Victoria", 'WA': "Western Australia",
          'TAS': "Tasmania", 'NT': "Northern Territory", 'SA': "South Australia", 'ACT': "Canberra",
          'NQ': "Cowboys!", 'NZ': "New Zealand"}

class Spinner(App):
    CurrentTripLocation = 'India'

    def build(self):
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('test_file.kv')
        return self.root

Spinner().run()