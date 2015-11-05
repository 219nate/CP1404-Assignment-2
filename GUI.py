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
    def __init__(self,**kwargs):
        super(App,self).__init__(**kwargs)
        self.tripCountryList = ["Belgium", "San Fransisco", "Australia"]

    def build(self):
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('GUI.kv')
        return self.root

    def updateConversionRate(self):

    def onSpinnerSelection(self):
        self.updateConversionRate()
        currentSpinner = self.root.ids.TripCountryNames.text


    def textBoxStatus(self, status=1):
        if status == 1:
            self.root.ids.HomeCountryAmount.disabled=False
            self.root.ids.CurrentCountryAmount.disabled = True
        else:
            self.root.ids.HomeCountryAmount.disabled = False
            self.root.ids.CurrentCountryAmount.disabled = False

    def onPress(self):
        print('buttonpress')
        self.textBoxStatus(0)


App().run()

