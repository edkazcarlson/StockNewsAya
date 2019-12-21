from textblob import TextBlob
from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl import worksheet
from openpyxl.utils.cell import get_column_letter
import os.path

class excelManager:
	def __init__(self, metaData):
		if os.path.exists('res/dataSheet.xlsx') :
			self.wb = load_workbook('res/dataSheet.xlsx')
			self.wb.save('res/dataSheet.xlsx')
		else: 
			self.wb = Workbook()
			firstTimeInit()
			self.wb.save('res/dataSheet.xlsx')
		self.metaData = metaData
		self.newTag(metaData)

	def firstTimeInit(self):
		self.stockPage = self.wb.active
		self.stockPage.title = "Stock Page"
		self.stockPage.cell(row=2, column=1, value='Average news score for the day')
		self.forexPage = self.wb.create_sheet(title = "Forex Page")
		self.forexPage.cell(row=2, column=1, value='Average news score for the day')
	
	def readMostRecentLine(self):
		print()
		
	def writeNewLine(self, todayDataDict):
		todaysColumn = self.stockPage.max_column
		curRow = 3
		for x in todayDataDict['Stocks']:
			self.stockPage.cell(row = curRow, column = todaysColumn, value = float(todaysResult[y]))
			++curRow
			for y in todayDataDict['Stocks'][x]:
				self.stockPage.cell(row = curRow, column = todaysColumn, value = todayDataDict['Stocks'][x][y])
				++curRow
		todaysColumn = self.stockPage.max_column
		curRow = 3
		for x in todayDataDict['Forex']:
			self.stockPage.cell(row = curRow, column = todaysColumn, value = float(todaysResult[y]))
			++curRow
			for y in todayDataDict['Forex'][x]:
				self.stockPage.cell(row = curRow, column = todaysColumn, value = todayDataDict['Forex'][x][y])
				++curRow
		
	def readXMostRecentLines(x):
		print()
		
	#returns a list of tags currently being used
	def getTags(self):
		return metaData
	
	#call when there's a new tag in order to add to the spreadsheet 
	def newTag(self, metaData):
		curRow = 3
		self.metaData = metaData
		for x in metaData['stocksWatched']:
			for y in stockDataTags:
				print(ws['A' + str(curRow)].value)
				if ws['A' + str(curRow)].value != x + ' ' + y: #if it changed, needs to move everything down 1
					ws.move_range('A' + str(curRow) + ':' + get_column_letter(ws.max_column) + str(ws.max_row), rows = 1, cols = 0)
				ws.cell(row=curRow, column=1, value=x + ' ' + y)
				curRow = curRow + 1
		for x in metaData['forexWatched']:
			print(x)
			for y in metaData['forexWatched'][x]:
				if ws['A' + str(curRow)].value != x + '->' + y: #if it changed, needs to move everything down 1
					ws.move_range('A' + str(curRow) + ':' + get_column_letter(ws.max_column) + str(ws.max_row), rows = 1, cols = 0)
				ws.cell(row=curRow, column=1, value=x + '->' + y)
				curRow = curRow + 1
			
	#call when there's a tag removed
	def removeTag(self, tagName):
		for x in metaData['stocksWatched']:
			for y in stockDataTags:
				print(ws['A' + str(curRow)].value)
				if ws['A' + str(curRow)].value != x + ' ' + y: #if it changed, needs to move everything down 1
					ws.move_range('A' + str(curRow) + ':' + get_column_letter(ws.max_column) + str(ws.max_row), rows = 1, cols = 0)
				ws.cell(row=curRow, column=1, value=x + ' ' + y)
				curRow = curRow + 1
		for x in metaData['forexWatched']:
			print(x)
			for y in metaData['forexWatched'][x]:
				if ws['A' + str(curRow)].value != x + '->' + y: #if it changed, needs to move everything down 1
					ws.move_range('A' + str(curRow) + ':' + get_column_letter(ws.max_column) + str(ws.max_row), rows = 1, cols = 0)
				ws.cell(row=curRow, column=1, value=x + '->' + y)
				curRow = curRow + 1