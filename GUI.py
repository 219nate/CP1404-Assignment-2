__author__ = 'Nathan Johnston'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.core.window import Window

Window.size = (300, 450)

class Spinner(App):
    TripCountryList = ["Belgium", "San Fransisco", "Austraia"]

    def build(self):
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('test_file.kv')
        return self.root

Spinner().run()
