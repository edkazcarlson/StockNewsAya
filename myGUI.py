import tkinter
from tkinter import *
from datetime import datetime

def settings(window, metaData):
	settingsWindow = tkinter.Tk()
	settingsWindow.title('Settings')
	
	settingsWindow.mainloop()

def buildMainGrid(window, metaData):
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
	settingsButton = Button(window, text = 'Settings', command = lambda: settings(window, metaData))
	settingsButton.grid(row = 0, column = 2, sticky = N)

def main(metaData):
	window = tkinter.Tk()
	buildMainGrid(window, metaData)
	window.mainloop()
  
if __name__== "__main__":
	main()

	