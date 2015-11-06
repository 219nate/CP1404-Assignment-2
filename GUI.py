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
        self.countryDictionary = get_complete_details()
        self.currentDate = time.strftime("%Y/%m/%d")

    def getTripDetails(self):
        trip=Details()
        tempCountryName=[]
        self.lineNumber=0
        file = open('config.txt', encoding='utf-8')
        for line in file:
            self.lineNumber+=1
            words = [word for word in line.strip().split(',')]
            try:
                self.countryDictionary[words[0]]
            except:
                self.root.ids.StatusMessage.text="Invalid Country"
                return
            if self.lineNumber>1:
                try:
                    trip.add((words[0]),(words[1]),(words[2]))
                    tempCountryName.append(words[0])
                except:
                    self.root.ids.StatusMessage.text="Invalid Date"
                    return
            else:
                self.homeCountry=words[0]
        self.tripCountryList=tempCountryName
        self.root.ids.TripCountryNamesSpinner.values=self.tripCountryList
        self.currentCountry=trip.current_country(time.strftime("%Y/%m/%d"))
        self.root.ids.HomeCountryStaticText.text=self.homeCountry

    def build(self):
        Config.set('graphics', 'resizable', '0')
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('GUI.kv')
        self.getTripDetails()
        return self.root

    def updateConversionRate(self):
        self.targetCountry = self.root.ids.TripCountryNamesSpinner.text
        if self.root.ids.TripCountryNamesSpinner.text == "":
            self.targetCountryCode = self.countryDictionary[self.currentCountry][1]
            self.root.ids.TripCountryNamesSpinner.text = self.currentCountry
        else:
            self.targetCountryCode = self.countryDictionary[self.root.ids.TripCountryNamesSpinner.text][1]
        self.homeCountryCode = self.countryDictionary[self.root.ids.HomeCountryStaticText.text][1]
        if self.countryDictionary[self.currentCountry][2]==self.countryDictionary[self.targetCountry][2]:
            self.homeToCountryRate=1
            self.countryToHomeRate=1
            self.root.ids.StatusMessage.text = "Updated at " + time.strftime("%H:%M:%S")
            return
        self.homeToCountryRate = convert(1,self.homeCountryCode,self.targetCountryCode)
        self.countryToHomeRate = convert(1,self.targetCountryCode,self.homeCountryCode)
        self.root.ids.StatusMessage.text = "Updated at " + time.strftime("%H:%M:%S")

    def onSpinnerSelection(self):
        self.textBoxStatus(0)
        self.updateConversionRate()

    def homeCountryAmountEntered(self):
        self.homeCountryAmount = self.root.ids.HomeCountryAmount.text
        try:
            self.homeCountryAmount = float(self.homeCountryAmount)
            self.convertedAmount = self.homeCountryAmount*self.homeToCountryRate
            self.root.ids.CurrentCountryAmount.text = "{0:.2f}".format(self.convertedAmount)
            self.homeCountryCode=self.countryDictionary[self.homeCountry][1]
            self.homeCurrencySymbol=(self.countryDictionary[self.homeCountry][2]).encode("utf-8")
            self.targetCountrySymbol=(self.countryDictionary[self.targetCountry][2]).encode("utf-8")
            self.conversionDirection="{} ({}) to {} ({})".format(self.homeCountryCode,self.homeCurrencySymbol,self.targetCountryCode,self.targetCountrySymbol)
            self.root.ids.StatusMessage.text=self.conversionDirection
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"



    def currentCountryAmountEntered(self):
        self.currentCountryAmount = self.root.ids.CurrentCountryAmount.text
        try:
            self.currentCountryAmount = float(self.currentCountryAmount)
            self.convertedAmount = self.currentCountryAmount*self.countryToHomeRate
            self.root.ids.HomeCountryAmount.text = "{0:.2f}".format(self.convertedAmount)
            self.homeCountryCode=self.countryDictionary[self.homeCountry][1]
            self.homeCurrencySymbol=(self.countryDictionary[self.homeCountry][2]).encode("utf-8")
            self.targetCountrySymbol=(self.countryDictionary[self.targetCountry][2]).encode("utf-8")
            self.conversionDirection="{} ({}) to {} ({})".format(self.targetCountryCode,self.targetCountrySymbol,self.homeCountryCode,self.homeCurrencySymbol)
            self.root.ids.StatusMessage.text=self.conversionDirection
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"


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
