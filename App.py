__author__ = 'Nathan Johnston 13019152'

#Import necessary modules
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from currency import *
from trip import *
import time

#Begin the App class
class App(App):
    #The initialiser function, variables were not created here,
    # instead they were created where they were needed to keep the code neat
    def __init__(self,**kwargs):
        super(App,self).__init__(**kwargs)
        # Run the module to create the dictionary of countries
        self.countryDictionary = get_complete_details()
        # Gets the current date to display to the GUI
        self.currentDate = time.strftime("%Y/%m/%d")

    #Function used to disable the text boxes if needed
    def disableBoxStatus(self, status=1):
        #If a value of 1 was given disable the text boxes
        if status == 1:
            self.root.ids.HomeCountryAmount.disabled=True
            self.root.ids.CurrentCountryAmount.disabled = True
        #Otherwise enable them, such as the case when the program is first initialised
        else:
            self.root.ids.HomeCountryAmount.disabled = False
            self.root.ids.CurrentCountryAmount.disabled = False

    #Function that uses the trip module in order to load the countries from the config file
    def getTripDetails(self):
        trip=Details()
        tempCountryName=[]
        self.lineNumber=0
        #If the file cannot be found display the error to the label
        try:
            file = open('config.txt', encoding='utf-8')
        except:
            self.root.ids.StatusMessage.text="Config not found"
        #Load the config file line at a time and add the name, start date and end date to the trip module. if that fails
        #then display an invalid config errror to the label
        try:
            for line in file:
                self.lineNumber+=1
                words = [word for word in line.strip().split(',')]
                #Check if the name of the trip is an actual country found in the country dictionary and display an error
                #if its not
                try:
                    self.countryDictionary[words[0]]
                except:
                    self.root.ids.StatusMessage.text="Invalid Country"
                    return
                #Add the trip to a temporary list if its not the first run through
                if self.lineNumber>1:
                    try:
                        trip.add((words[0]),(words[1]),(words[2]))
                        tempCountryName.append(words[0])
                    except:
                        self.root.ids.StatusMessage.text="Invalid Date"
                        return
                #If its the first iteration then set the first country in the config file to the home country
                else:
                    self.homeCountry=words[0]
        #If the config is invalid, lock the text box inputs
        except:
            self.root.ids.StatusMessage.text="Invalid Config"
            self.disableBoxStatus(1)
        #Set the trip country list which will be referenced by the spinner and update the spinner
        self.tripCountryList=tempCountryName
        self.root.ids.TripCountryNamesSpinner.values=self.tripCountryList
        #Use the trip module to find the country they are in depending on the trip details and the current date
        self.currentCountry=trip.current_country(time.strftime("%Y/%m/%d"))
        #Update the GUI accordingly
        self.root.ids.HomeCountryStaticText.text=self.homeCountry

    #Build the GUI
    def build(self):
        Config.set('graphics', 'resizable', '0')
        #Set the title and select main build file that the GUI will run from
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('GUI.kv')
        #Run the trip details to create the values for the spinner
        self.getTripDetails()
        #Set the desired window size
        Window.size = (350, 700)
        return self.root

    #Function that will update the conversion rate when the button is pressed or the spinner value is changed
    def updateConversionRate(self):
        self.targetCountry = self.root.ids.TripCountryNamesSpinner.text
        #If the spinner is blank, set it to the current country determined by the trip
        if self.root.ids.TripCountryNamesSpinner.text == "":
            self.targetCountryCode = self.countryDictionary[self.currentCountry][1]
            self.root.ids.TripCountryNamesSpinner.text = self.currentCountry
        #Otherwise use the country thats in the spinner
        else:
            self.targetCountryCode = self.countryDictionary[self.root.ids.TripCountryNamesSpinner.text][1]
        self.homeCountryCode = self.countryDictionary[self.root.ids.HomeCountryStaticText.text][1]
        #If the currency codes are they same dont waste time using the online converter
        if self.countryDictionary[self.currentCountry][2]==self.countryDictionary[self.targetCountry][2]:
            self.homeToCountryRate=1
            self.countryToHomeRate=1
            self.root.ids.StatusMessage.text = "Updated at " + time.strftime("%H:%M:%S")
            return
        #Tried to use the convert module to update the conversion rate
        try:
            #Uses the convert module to update conversion rates
            self.homeToCountryRate = convert(1,self.homeCountryCode,self.targetCountryCode)
            self.countryToHomeRate = convert(1,self.targetCountryCode,self.homeCountryCode)
            #Update the label to display the time it was updated at
            self.root.ids.StatusMessage.text = "Updated at " + time.strftime("%H:%M:%S")
        #If the conversion rate fails it locks the text boxes, which will remain locked until the conversion rate works
        except:
            self.root.ids.StatusMessage.text="Conversion Failed"
            self.disableBoxStatus(1)

    #When the spinner is changed, update the conversion rate and unlock the text boxes
    def onSpinnerSelection(self):
        self.disableBoxStatus(0)
        self.updateConversionRate()

    #When text is entered into the bottom text box convert the amount they entered and put it in the other text box
    def homeCountryAmountEntered(self):
        #Get the amount they entered
        self.homeCountryAmount = self.root.ids.HomeCountryAmount.text
        #Makes sure the input value is valid
        try:
            #Gets the input amount and converts it to type float
            self.homeCountryAmount = float(self.homeCountryAmount)
            #Multiply it by the conversion rate
            self.convertedAmount = self.homeCountryAmount*self.homeToCountryRate
            #Updates the other text box with the amount formatted to 2 decimal places
            self.root.ids.CurrentCountryAmount.text = "{0:.2f}".format(self.convertedAmount)
            #Sets the variables for the 3 digit code and the currency symbol which will be used in the label
            self.homeCountryCode=self.countryDictionary[self.homeCountry][1]
            self.homeCurrencySymbol=(self.countryDictionary[self.homeCountry][2]).encode("utf-8")
            self.targetCountrySymbol=(self.countryDictionary[self.targetCountry][2]).encode("utf-8")
            #Update the label to show the direction the currency was converted to and from
            self.conversionDirection="{} ({}) to {} ({})".format(self.homeCountryCode,self.homeCurrencySymbol,self.targetCountryCode,self.targetCountrySymbol)
            self.root.ids.StatusMessage.text=self.conversionDirection
        #If the input amount was invalid display an error to the label
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"

    #When text is entered into the top text box convert the amount they entered and put it in the other text box
    def currentCountryAmountEntered(self):
        #Get the amount they entered
        self.currentCountryAmount = self.root.ids.CurrentCountryAmount.text
        #Makes sure the input value is valid
        try:
            #Gets the input amount and converts it to type float
            self.currentCountryAmount = float(self.currentCountryAmount)
            #Multiply it by the conversion rate
            self.convertedAmount = self.currentCountryAmount*self.countryToHomeRate
            #Updates the other text box with the amount formatted to 2 decimal places
            self.root.ids.HomeCountryAmount.text = "{0:.2f}".format(self.convertedAmount)
            #Sets the variables for the 3 digit code and the currency symbol which will be used in the label
            self.homeCountryCode=self.countryDictionary[self.homeCountry][1]
            self.homeCurrencySymbol=(self.countryDictionary[self.homeCountry][2]).encode("utf-8")
            self.targetCountrySymbol=(self.countryDictionary[self.targetCountry][2]).encode("utf-8")
            #Update the label to show the direction the currency was converted to and from
            self.conversionDirection="{} ({}) to {} ({})".format(self.targetCountryCode,self.targetCountrySymbol,self.homeCountryCode,self.homeCurrencySymbol)
            self.root.ids.StatusMessage.text=self.conversionDirection
            #If the input amount was invalid display an error to the label
        except:
            self.root.ids.StatusMessage.text = "Invalid Amount"

    #Function that runs when the button is pressed
    def onPress(self):
        #Enable the text boxes
        self.disableBoxStatus(0)
        #Update the conversion rate
        self.updateConversionRate()
        #Clear the text boxes
        self.root.ids.HomeCountryAmount.text=""
        self.root.ids.CurrentCountryAmount.text=""


App().run()
