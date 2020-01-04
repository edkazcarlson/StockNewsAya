#Thank you to https://newsapi.org/ and https://www.alphavantage.co/ for the API being used here 
import requests
import json
import time
import os.path
import excelManager
from textblob import TextBlob
from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl import worksheet
from openpyxl.utils.cell import get_column_letter



stockDataTags = ['1. open', '2. high', '3. low',  '4. close','5. volume']
dataSheetLoc = 'res/dataSheet.xlsx'
metaDataPath = 'res/hist.json'

todaysDataDict = {None}

todayDateTime = datetime.now()
todayDay = todayDateTime.day 
todayYear = todayDateTime.year 
todayMonth = todayDateTime.month
todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)

#chcks if new URL is legal
def checkIfExists(urlToCheck):
	response = requests.get(urlToCheck).text
	return not 'Invalid API call.' in response
	# else:
		# metaData['stocksWatched'].append(enteredText)
		# with open(metaDataPath, 'w') as json_file:
			# json.dump(metaData, json_file)
			# #json_file.write(metaDataJSON)
		# return True 
		
	
#takes the newsApiKey and the data dict for today and adds today's news score to the data dict 
def getTodaysNews(newsApiKey, todaysDataDict):
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
	todaysDataDict['newsScore'] = str(todaysScore)
	return todaysDataDict

#Appends the data for the stocks being watched to todaysDataDict
def getTodaysStocks(stocksList, alphavantageApiKey, todaysDataDict):
	todaysDataDict['Stocks'] = {}
	marketOpen = True
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	for x in stocksList:
		stockURL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + x + '&apikey=' + alphavantageApiKey
		responseJSON = json.loads(requests.get(stockURL).text)
		print(responseJSON)
		if (responseJSON['Meta Data']['3. Last Refreshed'].find(todayString) == -1):
			marketOpen = False
			break
		todaysDataDict['Stocks'][x] = {}
		todaysResult = responseJSON['Time Series (Daily)'][todayString]
		for y in stockDataTags:
			todaysDataDict['Stocks'][x][y] = todaysResult[y]
		time.sleep(12)
	return marketOpen  

#Appends the data for the forex being watched to todaysDataDict
#forexToWatch is in the format from: {to1, to2}
def getForex(forexToWatch, alphavantageApiKey, todaysDataDict):
	todaysDataDict['Forex'] = {}
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	print('todayString todayString' + todayString)
	for x in forexToWatch:
		todaysDataDict['Forex'][x] = {}
		for y in forexToWatch[x]:
			forexURL = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='\
			+ x +'&to_currency='+ y +'&apikey=' + alphavantageApiKey
			responseJSON = json.loads(requests.get(forexURL).text)
			print(responseJSON)
			exchangeRate = responseJSON['Realtime Currency Exchange Rate']['5. Exchange Rate']
			print(x +' to ' + y + ' is ' + exchangeRate)
			todaysDataDict['Forex'][x][y] = exchangeRate
			time.sleep(12)
	return todaysDataDict
	
#adds the current date to todaysDataDict
def buildTodaysDate(todaysDataDict):
	todaysDataDict['todayDateStr'] =  todayString

#runs all the data collection functions and builds a dict based on them to pass to the excelManager in order to write to excel properly
def collectAll(metaData):
	todaysDataDict = dict()
	buildTodaysDate(todaysDataDict)
	getTodaysNews(metaData['newsApiKey'], todaysDataDict)
	marketOpen = getTodaysStocks(metaData['stocksWatched'], metaData['alphavantageApiKey'], todaysDataDict)
	getForex(metaData['forexWatched'], metaData['alphavantageApiKey'], todaysDataDict)
	
	manager = excelManager.excelManager(metaData, stockDataTags)
	manager.writeNewLine(todaysDataDict)
	manager.save()
	updateDateInHist()
	return marketOpen

def updateDateInHist():
	metaData = None
	lastDate = todayString
	newsApiKey = None
	alphavantageApiKey = None
	stocksList = None
	forexWatched = None
	with open(metaDataPath, "r") as json_file:
		metaData = json.load(json_file)	
		newsApiKey = metaData['newsApiKey']
		alphavantageApiKey = metaData['alphavantageApiKey']
		stocksList = metaData['stocksWatched']
		forexWatched = metaData['forexWatched']
	with open(metaDataPath, 'w') as json_file:
		metaDataDict = {'lastRan': lastDate,  'newsApiKey': newsApiKey, 'alphavantageApiKey': alphavantageApiKey, 'stocksWatched': stocksList, 'forexWatched': forexWatched}
		json.dump(metaDataDict, json_file)

#loads the metaData from metaData json 
def loadLocalData():
	todayDateTime = datetime.now()
	todayDay = todayDateTime.day 
	todayYear = todayDateTime.year 
	todayMonth = todayDateTime.month
	todayString = str(todayYear) + '-' + str(todayMonth).zfill(2) + '-' + str(todayDay).zfill(2)
	lastDate = ''
	newsApiKey = ''
	alphavantageApiKey = ''
	stocksList = []
	forexWatched = {}

	metaData = None 
	
	if not os.path.exists(metaDataPath): 
		with open(metaDataPath, 'w') as json_file:
			print('Meta data file not found, creating new.')
			metaDataDict = {'lastRan': todayString,  'newsApiKey': None, 'alphavantageApiKey': None, 'stocksWatched': ['DJI'], 'forexWatched': {'USD': ['JPY','EUR']}}
			json.dump(metaDataDict, json_file)
			#json_file.write(metaDataJSON)
	with open(metaDataPath, "r") as json_file:
		metaData = json.load(json_file)	
		lastDate = metaData['lastRan']
		newsApiKey = metaData['newsApiKey']
		alphavantageApiKey = metaData['alphavantageApiKey']
		stocksList = metaData['stocksWatched']
		forexWatched = metaData['forexWatched']
	print(lastDate)
	print(alphavantageApiKey)
	print(newsApiKey)
	return metaData
	
	#have the json be structured like:
	#newsApiKey
	#alphavantageApiKey
	#stocks watched:
		#stock name
	#commodities watched 
		#commodity name 
	#forex watched
		#forex names 



	
	
	
	