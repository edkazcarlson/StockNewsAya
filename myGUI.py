import json
import newsScraper
from tkinter import *
from datetime import datetime
from tkinter import messagebox



class stockSettingsWindow:
	def __init__(self, master, metaData):
		self.metaData = metaData
		self.alphavantageApiKey = metaData['alphavantageApiKey']
		thisWindow = Toplevel()
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
		if self.enteredText in self.metaData['stocksWatched']:
			messagebox.showinfo('Alert', 'Already being tracked')
		else :
			if newsScraper.checkIfExists('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + \
			str(self.enteredText) + '&apikey=' + self.alphavantageApiKey): #if its a legal stock  	
				with open(newsScraper.metaDataPath, 'w') as json_file:
					self.metaData['stocksWatched'].append(self.enteredText)
					print(self.metaData)
					json.dump(self.metaData, json_file)
					#json_file.write(metaDataJSON)
			else:
				messagebox.showinfo('Alert', 'Not a stock in the alphavantage database.')
				
class forexSettingsWindow:
	def __init__(self,master,metaData):
		self.metaData = metaData
		self.alphavantageApiKey = metaData['alphavantageApiKey']
		thisWindow = Toplevel()
		myForexList = Listbox(thisWindow)
		counter = 1
		for x in metaData['forexWatched']:
			myForexList.insert(counter,x + '->' + metaData['forexWatched'].get(x))
			counter += 1
		myForexList.grid(row = 0, column = 0, sticky = N)
		self.fromCurrency = Entry(thisWindow)
		self.fromCurrency.grid(row = 1, column = 0)
		self.toCurrency = Entry(thisWindow)
		self.toCurrency.grid(row = 1, column = 1)		
		self.entryButton = Button(thisWindow, text = 'Add new forex', command = self.getTextFromEntry)
		self.entryButton.grid(row = 1, column = 2)
		thisWindow.mainloop()
		
	def getTextFromEntry(self):
		self.fromCurrencyText = self.fromCurrency.get()
		self.fromCurrency.delete(0, 'end')
		self.toCurrencyText = self.toCurrency.get()
		self.toCurrency.delete(0, 'end')
		
		if self.fromCurrencyText in self.metaData['forexWatched'] and self.toCurrencyText == self.metaData['forexWatched'].get(self.fromCurrencyText):
			messagebox.showinfo('Alert', 'Already being tracked')
		else :
			if newsScraper.checkIfExists('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='\
			+ fromCurrencyText +'&to_currency='+ toCurrencyText +'&apikey=' + self.alphavantageApiKey): #if its a legal forex transaction  	
				with open(newsScraper.metaDataPath, 'w') as json_file:
					self.metaData['forexWatched'][fromCurrencyText] = 'toCurrencyText'
					print(self.metaData)
					json.dump(self.metaData, json_file)
					#json_file.write(metaDataJSON)
			else:
				messagebox.showinfo('Alert', 'Not a stock in the alphavantage database.')

class settingsWindow:	
	def __init__(self, master, metaData):
		self.metaData = metaData
		thisWindow = Toplevel()
		thisWindow.title('Settings')
		self.stockSettingsButton = Button(thisWindow, text = 'Check stocks being watched', command = self.stockSettings)
		self.stockSettingsButton.grid(row = 0, column = 0)
		self.forexSettingsButton = Button(thisWindow, text = 'Check forex being watched', command = self.forexSettings)
		self.forexSettingsButton.grid(row = 1, column = 0)
		thisWindow.mainloop()
	
	def stockSettings(self):
		stockWindow = stockSettingsWindow(self, self.metaData)
	
	def forexSettings(self):
		forexWindow = forexSettingsWindow(self,self.metaData)


class mainWindow:
	def __init__(self, metaData):
		self.metaData = metaData
		window = Tk()
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
		setting = settingsWindow(self, self.metaData)



def main():
	metaData = newsScraper.loadLocalData()
	guiWindow = mainWindow(metaData)

  
if __name__== "__main__":
	main()

	