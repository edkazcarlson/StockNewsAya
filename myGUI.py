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
		self.myStockList = Listbox(thisWindow)
		self.counter = 1
		for x in metaData['stocksWatched']:
			self.myStockList.insert(self.counter,x)
			self.counter += 1
		self.myStockList.grid(row = 0, column = 0, sticky = N)
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
				self.myStockList.insert(self.counter,self.enteredText)
				self.counter += 1
			else:
				messagebox.showinfo('Alert', 'Not a stock in the alphavantage database.')
				
class forexSettingsWindow:
	def __init__(self,master,metaData):
		self.metaData = metaData
		self.alphavantageApiKey = metaData['alphavantageApiKey']
		print(self.alphavantageApiKey)
		thisWindow = Toplevel()
		self.myForexList = Listbox(thisWindow)
		self.counter = 1
		for x in metaData['forexWatched']:
			for y in metaData['forexWatched'][x]:
				self.myForexList.insert(self.counter,x + '->' + y)
				self.counter += 1
		self.myForexList.grid(row = 0, column = 0, sticky = N)
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
		print(type(self.toCurrencyText))
		if self.fromCurrencyText in self.metaData['forexWatched'] and self.toCurrencyText in self.metaData['forexWatched'].get(self.fromCurrencyText):
			messagebox.showinfo('Alert', 'Already being tracked')
		else :
			if newsScraper.checkIfExists('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='\
			+ self.fromCurrencyText +'&to_currency='+ self.toCurrencyText +'&apikey=' + self.alphavantageApiKey): #if its a legal forex transaction  	
				with open(newsScraper.metaDataPath, 'w') as json_file:
					if self.fromCurrencyText in self.metaData['forexWatched']:
						self.metaData['forexWatched'][self.fromCurrencyText].append(self.toCurrencyText)
						print(self.metaData)
						json.dump(self.metaData, json_file)
						#json_file.write(metaDataJSON)
					else:
						self.metaData['forexWatched'][self.fromCurrencyText] = [self.toCurrencyText]
						print(self.metaData)
						json.dump(self.metaData, json_file)
				self.myForexList.insert(self.counter,self.fromCurrencyText + '->' + self.toCurrencyText)
				self.counter += 1
			else:
				messagebox.showinfo('Alert', 'Not a currency exchange in the alphavantage database.')

class settingsWindow:	
	def __init__(self, master, metaData):
		self.metaData = metaData
		thisWindow = Toplevel()
		thisWindow.title('Settings')
		self.stockSettingsButton = Button(thisWindow, text = 'Check stocks being watched', command = self.stockSettings)
		self.stockSettingsButton.grid(row = 0, column = 0)
		self.forexSettingsButton = Button(thisWindow, text = 'Check forex being watched', command = self.forexSettings)
		self.forexSettingsButton.grid(row = 0, column = 1)
		self.apiKeySettingsButton = Button(thisWindow, text = 'Change or set API keys', command = self.setApiKeys)
		self.apiKeySettingsButton.grid(row = 1, column = 0)
		thisWindow.mainloop()
	
	def stockSettings(self):
		stockWindow = stockSettingsWindow(self, self.metaData)
	
	def forexSettings(self):
		forexWindow = forexSettingsWindow(self,self.metaData)
		
	def setApiKeys(self):
		apiWindow = apiSettings(self, self.metaData)
	
class apiSettings:
	def __init__(self,master,metaData):
		self.metaData = metaData
		thisWindow = Toplevel()
		thisWindow.title('API Key Settings')
		self.enteredText = ''
		self.newsAPIentry = Entry(thisWindow)
		self.newsAPIentry.grid(row = 0, column = 0)
		self.newsAPIButton = Button(thisWindow, text = 'Set newsAPI key', command = self.newsAPISet)
		self.newsAPIButton.grid(row = 0, column = 1)
		
		self.alphavantageentry = Entry(thisWindow)
		self.alphavantageentry.grid(row = 1, column = 0)
		self.alphavantageButton = Button(thisWindow, text = 'Set alphavantage key', command = self.alphavantageAPISet)
		self.alphavantageButton.grid(row = 1, column = 1)
		thisWindow.mainloop()
	
	def newsAPISet(self):
		self.enteredText = self.newsAPIentry.get()
		self.newsAPIentry.delete(0, 'end')
		with open(newsScraper.metaDataPath, 'w') as json_file:
			self.metaData['newsApiKey'] = self.enteredText
			json.dump(self.metaData, json_file)

	def alphavantageAPISet(self):
		self.enteredText = self.alphavantageentry.get()
		self.alphavantageentry.delete(0, 'end')
		with open(newsScraper.metaDataPath, 'w') as json_file:
			self.metaData['alphavantageApiKey'] = self.enteredText
			json.dump(self.metaData, json_file)

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
		getTodayButton = Button(window, text = 'Get todays data', command = lambda: self.getTodayData())
		getTodayButton.grid(row = 1, column = 0, sticky = N)		
		window.mainloop()
	
	def openSettings(self):
		setting = settingsWindow(self, self.metaData)
		
	def getTodayData(self):
		print()



def main():
	metaData = newsScraper.loadLocalData()
	guiWindow = mainWindow(metaData)
	#newsScraper.buildBoardLabels('hi', 'hi', metaData, 'hi')

  
if __name__== "__main__":
	main()

	