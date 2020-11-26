#-*- coding: utf-8 -*-

#importando os módulos do chatbot
import time
import os
import requests
import json
import speech_recognition as sr
import pyttsx3
import http.client
import tempfile
import win32api
import win32print


from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def checkGmail():
   
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    

    if not messages:
        speak ("No messages found.")
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            for temp in msg['payload'].get('headers'):
                if 'From' in temp.get('name'):
                    a=temp.get('value').split('<')
                    speak ('Email de: '+a[0])
            speak (msg['snippet'])


def printFile(nome, n):
	if n == 'duas':
		n = 2
	if n == 'uma':
		n=1
	for i in range (int(n)):
		win32api.ShellExecute (0,"print",findFiles(nome),'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
		time.sleep(10)

def speak(text):
	speaker.setProperty('voice', 'brazil')
	speaker.setProperty('rate', 150) 
	speaker.say(text)
	speaker.runAndWait()

def idLeague(league):
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '6f85448cae8846b38a93712b9bb65a38' }
	connection.request('GET', '/v2/competitions/', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	leagues = response.get("competitions")
	if 'brasileiro' in league.lower():
		return (2013)
	else:
		for temp in leagues:			
			if league.lower() in temp.get("name").lower():
				return (temp.get("id"))				


def posTime(team, league):
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '6f85448cae8846b38a93712b9bb65a38' }
	connection.request('GET', '/v2/competitions/'+str(idLeague(league)) +'/standings', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	table = response.get("standings")[0].get("table")
	for temp in table:
		if team.lower() in temp.get("team").get("name").lower():
			return (temp.get("team").get("name"), temp.get("position"), temp.get("id"))

def selectTeamLeague(string):
	temp= speech.split()
	for i, value in enumerate (temp):
		if value == 'no' or value == 'na':
			if temp[i-2] != 'da' and temp[i-2]!='do':
				team = temp[i-2] + " " + temp[i-1]
			else:
				team = temp[i-1]
			league =  temp[i+1] + ' ' + temp[i+2]
			return (team, league)

r = sr.Recognizer()

def findFiles(filename):
	search_path = "C:/Users/mathe/OneDrive/Documentos"
	for root, dir, files in os.walk(search_path):
		for temp in files:
			if temp.lower().startswith(filename.lower()):
				return (os.path.join(root, temp))
			
speaker = pyttsx3.init()
with sr.Microphone() as s:
	r.adjust_for_ambient_noise(s)
	while True:
		#try:
			audio = r.listen(s)
			speech = r.recognize_google(audio, language='pt')
			print(speech)
			if 'ações' in speech and 'preço' in speech:
				empresa = speech.split()[len(speech.split())-1]
				print(empresa)
				url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + empresa + '.SA?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
				data = (requests.get(url))
				priceNow = (data.json()['chart']['result'][0]['meta']['regularMarketPrice'])
				pricePreviousClose = (data.json()['chart']['result'][0]['meta']['previousClose'])
				variation = (priceNow/pricePreviousClose)-1
				variation = "{:.2%}".format(variation)
				speak('O valor desta ação é de: '+ str(priceNow) + ', e variou: ' + variation)										

			if 'posição' in speech or 'lugar' in speech:
				temp= selectTeamLeague(speech)
				pos =posTime(temp[0],temp[1])
				speak ('O ' + pos [0] + ' está na ' + str(pos[1]) +'ª posição')

			if 'imprim' in speech:
				temp = speech.split()
				for i, string in enumerate(temp):
					if 'arquivo' in string:
						arquivo = temp[i+1]
					if 'imprim' in string:
						n = temp[i+1]
						if n == 'o':
							n =1
				printFile(arquivo, n)
				speak('Os arquivos ja foram impressos')

			if 'e-mail' in speech:
				
				temp = speech.split()
				for i, string in enumerate(temp):
					if 'email' in temp:
						n = temp[i-1]
				checkGmail()

		#except:
		#	speak('Não entendi')
		