import json
import tkinter
from tkinter import *
from datetime import datetime

def checkIfExists(urlToCheck):
	response = requests.get(urlToCheck).text
	return not ('Invalid API call.' in response)


class stockSettingsWindow:
	def __init__(self, master, metaData):
		self.metaData = metaData
		thisWindow = tkinter.Toplevel()
		thisWindow.title('Stock Settings')
		myStockList = Listbox(thisWindow)
		counter = 1
		for x in metaData['stocksWatched']:
			myStockList.insert(counter,x)
			counter += 1
		myStockList.grid(row = 0, column = 0, sticky = N)
		self.enteredText = ''
		self.entry = Entry(thisWindow)
		self.entry.grid(row = 1, column = 0)
		self.entryButton = Button(thisWindow, text = 'Add new stock', command = self.getTextFromEntry)
		self.entryButton.grid(row = 1, column = 1)
		thisWindow.mainloop()
	
	def getTextFromEntry(self):
		self.enteredText = self.entry.get()
		self.entry.delete(0, 'end')
		if checkIfExists(self.metaData, \
		'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + str(self.enteredText) + '&apikey=' + str(self.metaData['alphavantageApiKey'])):
			self.metaData['stocksWatched'].append(self.enteredText)
			
	
	 
class mainWindow:
	def __init__(self, metaData):
		self.metaData = metaData
		window = tkinter.Tk()
		todayDateTime = datetime.now()
		todayDay = todayDateTime.day 
		todayYear = todayDateTime.year 
		todayMonth = todayDateTime.month
		todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
		window.title('Market tracker') 
		menu = Menu(window)
		todayLabel = Label(window, text = 'Today is: ' + todayString)
		todayLabel.grid(row = 0, column = 0, sticky = N )
		yesterdayLabel = Label(window, text = 'Last ran: ' + metaData['lastRan'])
		yesterdayLabel.grid(row = 0, column = 1, sticky = N )
		settingsButton = Button(window, text = 'Settings', command = lambda: self.openSettings())
		settingsButton.grid(row = 0, column = 2, sticky = N)
		window.mainloop()
	
	def openSettings(self):
		settingsWindow = stockSettingsWindow(self, self.metaData)



def main(metaData):
	guiWindow = mainWindow(metaData)
	
  
if __name__== "__main__":
	main()

	