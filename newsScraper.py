#Thank you to https://newsapi.org/ and https://www.alphavantage.co/ for the API being used here 
import requests
import json
import time
import os.path
import myGUI
from textblob import TextBlob
from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from openpyxl import load_workbook


stockDataTags = ['1. open', '2. high', '3. low',  '4. close','5. volume']
dataSheetLoc = 'res/dataSheet.xlsx'

todaysDataDict = {None}


def buildBoardLabels(wb, ws, alphaStocks, alphaStockTags, dataSheetLoc):
	curRow = 2
	ws.cell(row=curRow, column=1, value='Average news score for the day')
	curRow = curRow + 1
	for x in alphaStocks:
		for y in alphaStockTags:
			ws.cell(row=curRow, column=1, value=x + ' ' + y)
			curRow = curRow + 1
	ws.cell(row=curRow, column=1, value='Price of gold per troy ounce')
	curRow = curRow + 1
	ws.cell(row=curRow, column=1, value='Price of silver per troy ounce')
	curRow = curRow + 1
	#wb.save(dataSheetLoc)
	
def getTodaysNews(wb,ws,newsApiKey, todaysDataDict):
	print("doo doo water: " + str(ws.max_column))
	listOfBuisnessNewsURL = 'https://newsapi.org/v2/sources?language=en&category=business&apiKey=' + newsApiKey
	oneDayForward = datetime.now() + timedelta(days=1) 
	oneDayForwardYear = str(oneDayForward.year)
	oneDayForwardMonth = str(oneDayForward.month)
	oneDayForwardDay = str(oneDayForward.day) 
	oneDayBack = datetime.now() - timedelta(days=1) 
	oneDayBackYear = str(oneDayBack.year)
	oneDayBackMonth = str(oneDayBack.month)
	oneDayBackDay = str(oneDayBack.day) 
	
	listOfBuisnessNews = set();
	responseJSON = json.loads(requests.get(listOfBuisnessNewsURL).text)
	for x in responseJSON['sources']:
		listOfBuisnessNews.add(x['id'])
	#print(listOfBuisnessNews)


	todaysTotalScore = 0
	articlesParsed = 0
	for x in listOfBuisnessNews:
		recentFromXURL = 'http://newsapi.org/v2/everything?sources=' + x + '&from='+ \
		oneDayBackYear + '-'+ oneDayBackMonth +'-'+ oneDayBackDay +'&to='+ \
		oneDayForwardYear +'-'+ oneDayForwardMonth +'-'+ oneDayForwardDay +'&ApiKey=' + newsApiKey
		responseJSON = json.loads(requests.get(recentFromXURL).text)
		for article in responseJSON['articles']:
			articlesParsed = articlesParsed + 1
			titleScore = TextBlob(article['title'])
			#print(titleScore.sentiment.polarity )
			todaysTotalScore += titleScore.sentiment.polarity  #get an api key from https://www.alphavantage.co/
			#print(article['title'])
			#print("xd rawr")
	todaysScore = todaysTotalScore / articlesParsed
	print("todays score is: " + str(todaysScore))
	todaysDataDict['newsScore': str(todaysScore)]
	return todaysDataDict

def getTodaysStocks(wb, ws, stocksList,stockDataTags, alphaAdvantageApiKey, todaysColumn, curRow):
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	for x in stocksList:
		stockURL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + x + '&apikey=' + alphaAdvantageApiKey
		responseJSON = json.loads(requests.get(stockURL).text)
		print(responseJSON)
		if (responseJSON['Meta Data']['3. Last Refreshed'].find(todayString) == -1):
			print(responseJSON['Meta Data']['3. Last Refreshed'])
			print(todayString)
			print("Market was not open today")
			print(x)
			print(responseJSON['Meta Data']['3. Last Refreshed'].find(todayString))
			break
		todaysResult = responseJSON['Time Series (Daily)'][todayString]
		for y in stockDataTags:
			ws.cell(row = curRow, column = todaysColumn, value = float(todaysResult[y]))
			curRow = curRow + 1
		time.sleep(12)
	return curRow  

	
def getForex(wb,ws,alphaAdvantageApiKey, forexToWatch, todaysColumn, curRow):
	print(testStr)
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	print('todayString todayString' + todayString)
	for x in forexToWatch:
		forexURL = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='\
		+ x +'&to_currency='+ forexToWatch[x]+'&apikey=' + alphaAdvantageApiKey
		responseJSON = json.loads(requests.get(forexURL).text)
		print(responseJSON)
		exchangeRate = responseJSON['Realtime Currency Exchange Rate']['5. Exchange Rate']
		print(x +' to ' + forexToWatch[x] + ' is ' + exchangeRate)
	
	
	
def buildTodaysData(newsApiKey, alphaAdvantageApiKey, stocksList, stockDataTags, forexToWatch, todaysDataDict):
	todayDateTime = datetime.now()
	todayDay = todayDateTime.day 
	todayYear = todayDateTime.year 
	todayMonth = todayDateTime.month
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	todaysDataDict['todayDateStr' : todayString]
	

def loadLocalData():
	todayDateTime = datetime.now()
	todayDay = todayDateTime.day 
	todayYear = todayDateTime.year 
	todayMonth = todayDateTime.month
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	lastDate = ''
	newsApiKey = ''
	alphaAdvantageApiKey = ''
	stocksList = []
	forexWatched = {}

	metaData = None 
	metaDataPath = 'res/hist.json'
	if not os.path.exists(metaDataPath): 
		with open(metaDataPath, 'w') as json_file:
			print('Meta data file not found, creating new.')
			metaDataDict = {'lastRan': todayString,  'newsApiKey': None, 'alphaAdvantageApiKey': None, 'stocksWatched': ['DJI'], 'forexWatched': [None]}
			json.dump(metaDataDict, json_file)
			#json_file.write(metaDataJSON)
	with open(metaDataPath, "r") as json_file:
		metaData = json.load(json_file)	
		lastDate = metaData['lastRan']
		newsApiKey = metaData['newsApiKey']
		alphaAdvantageApiKey = metaData['alphaAdvantageApiKey']
		stocksList = metaData['stocksWatched']
		forexWatched = metaData['forexWatched']
	print(lastDate)
	print(alphaAdvantageApiKey)
	print(newsApiKey)
	return metaData
	
	#have the json be structured like:
	#newsApiKey
	#alphaAdvantageApiKey
	#stocks watched:
		#stock name
	#commodities watched 
		#commodity name 
	#forex watched
		#forex names 
		





# wb = Workbook()
# ws = wb.active

# if (os.path.exists(dataSheetLoc) ):
	# wb = load_workbook(dataSheetLoc)
	# ws = wb.active
	# if (not ws.max_row == 2 + (len(stocksList) * len(stockDataTags))):
		# buildBoardLabels(wb,ws,stocksList, stockDataTags, dataSheetLoc)
# else:
	# buildBoardLabels(wb,ws,stocksList, stockDataTags, dataSheetLoc)


# if (ws.cell(row = 1, column =ws.max_column).value == str(todayDay) + '-' + str(todayMonth) + '-' + str(todayYear)):
	# print("Already ran today")
# else:
	# print('cell val: ' + str(ws.cell(row = 1, column =ws.max_column + 1).value))
	# print('cell val2: ' + str(ws.cell(row = 5, column =ws.max_column).value))
	# print(str(ws.max_column))
	# print(str(ws.max_row))
	# todaysColumn = ws.max_column
	# endingRow = getTodaysNews(wb, ws, newsApiKey, todaysColumn)
	# endingRow = getTodaysStocks(wb, ws, stocksList, alphaAdvantageApiKey, todaysColumn, endingRow)
	# getCommodities(wb, ws ,todaysColumn, endingRow)
# wb.save(dataSheetLoc)

def main():
	metaData = loadLocalData()
	myGUI.main(metaData)
 

if __name__== "__main__":
  main()