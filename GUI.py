__author__ = 'Nathan Johnston'
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.core.window import Window
from currency import *
from web_utility import *
from trip import *
import time

Window.size = (350, 700)

class App(App):
    def __init__(self,**kwargs):
        super(App,self).__init__(**kwargs)
        self.tripCountryList = ["Belgium", "San Fransisco", "Australia", "Japan"]
        self.countryDictionary = get_complete_details()
        self.currentDate = time.strftime("%Y/%m/%d")

    def build(self):
        Config.set('graphics', 'resizable', '0')
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('GUI.kv')
        return self.root

    def updateConversionRate(self):
        if self.root.ids.TripCountryNamesSpinner.text == "":
            self.targetCountry = "Australia" #!!! MAKE IT SET THE TARGET AREA TO THE CURRENT TRIP DATE PLACE
            self.root.ids.TripCountryNamesSpinner.text = self.targetCountry
        else:
            self.targetCountry = self.root.ids.TripCountryNamesSpinner.text
        self.homeCountry = self.root.ids.HomeCountryStaticText.text
        self.homeToCountryRate = convert(1,self.homeCountry,self.targetCountry)
        self.countryToHomeRate = convert(1,self.targetCountry,self.homeCountry)
        self.root.ids.StatusMessage.text = "Updated at " + time.strftime("%H:%M:%S")

    def onSpinnerSelection(self):
        self.textBoxStatus(0)
        self.updateConversionRate()

    def homeCountryAmountEntered(self):
        self.homeCountryAmount = self.root.ids.HomeCountryAmount.text
        try:
            self.homeCountryAmount = float(self.homeCountryAmount)
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"
        self.convertedAmount = self.homeCountryAmount*self.homeToCountryRate
        self.root.ids.CurrentCountryAmount.text = str(self.convertedAmount)

    def currentCountryAmountEntered(self):
        self.currentCountryAmount = self.root.ids.CurrentCountryAmount.text
        try:
            self.currentCountryAmount = float(self.currentCountryAmount)
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"
        self.convertedAmount = self.currentCountryAmount*self.countryToHomeRate
        self.root.ids.HomeCountryAmount.text = str(self.convertedAmount)

    def textBoxStatus(self, status=1):
        if status == 1:
            self.root.ids.HomeCountryAmount.disabled=False
            self.root.ids.CurrentCountryAmount.disabled = True
        else:
            self.root.ids.HomeCountryAmount.disabled = False
            self.root.ids.CurrentCountryAmount.disabled = False

    def onPress(self):
        self.textBoxStatus(0)
        self.updateConversionRate()


App().run()

