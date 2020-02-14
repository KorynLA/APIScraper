import requests
import sys
import json
import csv
import re
import socket

def getResponse(URL):
	response = requests.get(url=URL, params=PARAMS)
	parseResponse=json.loads(response.text)
	return [parseResponse, response.status_code]

#Excel will have [Job Name, Company Name, City, State, Contents, Web Address]
def placeInExcel(parseResponse):
	with open('jobs.csv', 'a') as writeCsv:
		filewriter = csv.writer(writeCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		name=str(parseResponse["name"]).replace('\n', ' ').replace('\r', '')
		company=str(parseResponse["company"]["name"]).replace('\n', ' ').replace('\r', '')
		location=""
		locationGiven = lambda parseResponse : True if(len(parseResponse["locations"]) != 0) else False
		if(locationGiven(parseResponse) == True):
			location=str(parseResponse["locations"][0]["name"]).replace('\n', ' ').replace('\r', '')
		contents=str("")
		link=str(parseResponse["refs"]["landing_page"])
		if(re.search("software",parseResponse["contents"]) != None or re.search("software",name) != None):
			filewriter.writerow([name, company, location, contents, link])

#The Muse data retrieved as JSON
def theMuse():
	pageNumber=1
	while(True):
		URL="https://www.themuse.com/api/public/jobs?level=Internship&level=Entry%20Level&page="+str(pageNumber)+"&descending=true"
		parseResponse=getResponse(URL)
		if parseResponse[1] != 200: 
			print(parseResponse[1])
			break
		for i in range(len(parseResponse[0]["results"])):
			placeInExcel(parseResponse[0]["results"][i])
		pageNumber+=1

#Indeed data retrieved as XML, waiting on API key
def indeed():
	hostName=socket.gethostname()
	ipAddr=socket.gethostbyname(hostname)
	PARAMS= {
	'publisher':'',
	'v':'2',
	'userip': ipAddr,
	'useragent':'Mozilla/%2F4.0%28Firefox%29'
	}

reload(sys)
sys.setdefaultencoding('UTF-8')
with open('jobs.csv', 'wb') as writeCsv:
	filewriter = csv.writer(writeCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['Title', 'Company', 'City', 'State' ,'Contents', 'Link'])
theMuse()