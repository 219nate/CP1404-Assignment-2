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

file = open("config.txt", encoding="utf-8")
for line in file:
            words = [word for word in line.strip().split(',')]
            trip=Details()
            trip.add(words[0],words[1],words[2])

class App(App):
    def __init__(self,**kwargs):
        super(App,self).__init__(**kwargs)
        self.countryDictionary = get_complete_details()
        self.currentDate = time.strftime("%Y/%m/%d")

    def build(self):
        Config.set('graphics', 'resizable', '0')
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('GUI.kv')
        self.tripCountryList=[]
        return self.root


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


    def updateConversionRate(self):
        self.getTripDetails()
        if self.root.ids.TripCountryNamesSpinner.text == "":
            self.targetCountry = self.countryDictionary[self.currentCountry][1]
            self.root.ids.TripCountryNamesSpinner.text = self.currentCountry
        else:
            self.targetCountry = self.countryDictionary[self.root.ids.TripCountryNamesSpinner.text][1]
        self.homeCountry = self.countryDictionary[self.root.ids.HomeCountryStaticText.text][1]
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
            self.convertedAmount = self.homeCountryAmount*self.homeToCountryRate
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"
        self.root.ids.CurrentCountryAmount.text = str(self.convertedAmount)

    def currentCountryAmountEntered(self):
        self.currentCountryAmount = self.root.ids.CurrentCountryAmount.text
        try:
            self.currentCountryAmount = float(self.currentCountryAmount)
            self.convertedAmount = self.currentCountryAmount*self.countryToHomeRate
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"
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

print(trip)