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
import win32com.client
import pyautogui
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from urllib.request import Request, urlopen  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def openProgram(program):
	try:
		speak("Abrindo " + program)
		os.system('"' +findFiles(program,1) + '"')
	except:
		speak("Erro ao abrir " + program)

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
		win32api.ShellExecute (0,"print",findFiles(nome,0),'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
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

def findFiles(filename, n):
	results = []
	results2 = []
	pastas = []
	exts = []
	if n == 0:
		search_path = "C:\\Users\\mathe\\OneDrive\\Documentos"
	if n==1:
		search_path = "C:\\Users\\mathe\\Atalhos"
	for root, dir, files in os.walk(search_path):
		for temp in files:
			if temp.lower().startswith(filename.lower()):
				results.append([root, temp])
	if len(results) > 1:
		for result in results:
			temp = result[0].split("\\")
			pasta = temp[len(temp)-1]
			if len(pastas)>0 and pasta != pastas[len(pastas)-1]:
				pastas.append(pasta)
			if len(pastas) ==0:
				pastas.append(pasta)
				
		if len(pasta)> 1:
			print (pastas)
			speak ("O arquivo está na pasta ")
			for i, a in enumerate (pastas):
				if i == len(pastas)-1:
					speak(a)
				else:
					speak(a + ", ou na pasta ")
			with sr.Microphone() as s:
				speech = ''
				while  speech == '':
					try:
						r.adjust_for_ambient_noise(s)
						audio = r.listen(s)
						speech = r.recognize_google(audio, language='pt')
						print (speech)
					except:
						speak("Não entendi")
				for a in pastas:
					if speech.lower() in a.lower():
						for c, b in enumerate (results):
							t = b[0].split('\\')
							j = t[len(t)-1]
							if j == a:
								results2.append(results[c])
		
		if len(results2)>1 or results2 == []:
			if(results2 != []):
				results = results2
				results2 = []
			for result in results:
				temp = result[1].split(".")
				ext = temp[len(temp)-1]
				print (temp)
				if len(exts)>0 and ext != exts[len(exts)-1]:
					exts.append(ext)					
				if len(exts) ==0:
					exts.append(ext)
			if len(ext)> 1:
				speak ("A extensão do arquivo é: ")
				for i, a in enumerate (exts):
					if i == len(exts)-1:
						speak(a)
					else:
						speak(a + ", ou ")
				with sr.Microphone() as s:
					speech = ''
					while  speech == '':
						try:
							r.adjust_for_ambient_noise(s)
							audio = r.listen(s)
							speech = r.recognize_google(audio, language='pt')
							print (speech)
							if 'doc X' in speech or 'doki' in speech:
								speech = 'docx'
							for a in exts:
								if speech.lower() in a.lower():
									for c, b in enumerate (results):
										t = b[1].split('.')
										j = t[len(t)-1]
										if j == a:
											results2.append(results[c])
						except:
							speak("Não entendi")
				results = results2
	print(results)
			
	return (results[0][0] + "\\" + results[0][1])

def googleSearch(string):

	browser = webdriver.Chrome(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis/chromedriver')
	browser.get('http://www.google.com')
	
	elementoEntrada = browser.find_element_by_css_selector('.gLFyf.gsfi') # procura o elemento
	elementoEntrada.send_keys(string) # preenche com a palavra amazonia
	elementoEntrada.submit() # realiza a pesquisa
	

	return browser.current_url

def nextMatch(string):
	req = Request(googleSearch(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")

	times = soup.find_all('div', class_="ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx")
	jogo = []
	for time in times:
		jogo.append(time.find('span').string)
	temp = ('o próximo jogo é: ' + jogo[0] + 'contra ' + jogo[1])
	speak(temp)

def whoIs(string):
	req = Request(googleSearch(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	resp = soup.find_all('span', class_="hgKElc")
	for temp in resp:
		speak(temp.get_text())

def stockValue(string):
	req = Request(googleSearch(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	resp = soup.find_all('span', class_="vWLAgc")
	speak (resp.get_text)
	

r = sr.Recognizer()			
speaker = pyttsx3.init()
with sr.Microphone() as s:
	r.adjust_for_ambient_noise(s)
	while True:
		#try:
			audio = r.listen(s)
			speech = r.recognize_google(audio, language='pt')
			speech = speech.lower()
			print(speech)

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
						if n == 'o' or n == 'arquivo':
							n =1
				printFile(arquivo, n)
				speak('Os arquivos foram impressos')

			if 'e-mail' in speech:
				
				temp = speech.split()
				for i, string in enumerate(temp):
					if 'email' in temp:
						n = temp[i-1]
				checkGmail()

			if 'abr' in speech :
				temp = speech.split()
				for i, word in enumerate (temp):
					if 'abr' in word:
						if temp[i+1] == 'o' or temp[i+1] =='a:':
							openProgram(temp[i+2])
						else:
							openProgram(temp[i+1])
			if 'música' in speech:
				if 'pausa' in speech or 'para' in speech or 'solta' in speech or 'toca':
					pyautogui.press('playpause')
				if 'próxim' in speech:
					pyautogui.press('nexttrack')
				if 'volta' in speech or 'repete' in speech:
					pyautogui.press('prevtrack')
				if 'anterior' in speech:
					pyautogui.press('prevtrack')
					pyautogui.press('prevtrack') 
			if 'pesquisa' in speech:
				temp = speech.split()
				a = ''
				for i, word in enumerate(temp):
					if i>0:
						a+= word + ' '
				if 'próxim' in a and ('jogo' in a or 'partida' in a):
					nextMatch(a)
				if 'quem é' in a:
					whoIs(a)
				if 'ações' in speech and 'preço' in speech:
					stockValue (a)

		#except:
		#	speak('Não entendi')
		