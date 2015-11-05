__author__ = 'Nathan Johnston'
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.core.window import Window
from currency import *
from web_utility import *
from trip import *

Window.size = (300, 450)

class App(App):
    def __init__(self):
        self.tripCountryList = ["Belgium", "San Fransisco", "Australia"]

    def textBoxStatus(self, status=1):
        if status == 1:
            self.true.ids.HomeCountryAmount.disabled=True
            self.true.ids.CurrentCountryAmount.disabled=True
        else:
            self.true.ids.HomeCountryAmount.disabled=False
            self.true.ids.CurrentCountryAmount.disabled=False

    def build(self):
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('GUI.kv')
        return self.root

    def onPress(self):
        print('buttonpress')
        self.textBoxStatus(0)

App().run()

