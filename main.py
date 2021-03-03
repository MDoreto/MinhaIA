#region Import

import time
import os
import json
import speech_recognition as sr
import pyttsx3
import http.client
import tempfile
import win32com.client
import pyautogui
from urllib.request import Request, urlopen  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
import nltk
import unidecode
from pywebostv.discovery import * 
from pywebostv.connection import *
from pywebostv.controls import *
import time
import _thread
import datetime as dt
import pickle
from datetime import datetime  
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as req

#endregion

#region MachineLearning

def training(genre):
	base = []
	manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','r', encoding="utf8")
	for lines in manipulador.readlines():
		temp = lines.rstrip('\n').split(',')
		if genre =='':
			t = (temp[0].lower(),temp[2])
			base.append(t)
		elif (temp[2] == genre):
			t = (temp[0].lower(),temp[1])
			base.append(t)
	manipulador.close()
	frasescomstemming = fazstemmer(base)
	frequencia = buscafrequencia(buscapalavras(frasescomstemming))
	global palavrasunicas
	if genre =='':
		palavrasunicas = busca_palavrasunicas(frequencia)
	basecompleta = nltk.classify.apply_features(extrai_palavras,frasescomstemming)
	return nltk.NaiveBayesClassifier.train(basecompleta) 				 

def classify (classificador, string):
	testestem = []
	for (palavras) in string.split():
		comstem = [p for p in palavras.split()]
		testestem.append(str(stemmer.stem(comstem[0])))
	nova_frase = extrai_palavras(testestem)		
	distribuicao = classificador.prob_classify(nova_frase)		
	method = ['',0]
	for classe in distribuicao.samples():
		if distribuicao.prob(classe) > method[1]:
			method[0] = classe
			method[1] = distribuicao.prob(classe)
	return method[0]

def fazstemmer(texto):
	stemmer = nltk.stem.RSLPStemmer() 
	frasessstemming = []
	for (palavras, emocao) in texto:
		comstemming = [str(stemmer.stem(p))
					   for p in palavras.split() if p not in stopwords]
		frasessstemming.append((comstemming, emocao))
	return frasessstemming

def buscapalavras(frases):
	todaspalavras = []
	for (palavras, emocao) in frases:
		todaspalavras.extend(palavras)
	return todaspalavras
 
def buscafrequencia(palavras):
	palavras = nltk.FreqDist(palavras)
	return palavras
	
def busca_palavrasunicas(frequencia):
	freq = frequencia.keys()
	return freq

def extrai_palavras(documento):
	doc = set(documento)
	caracteristicas = {}
	for palavras in palavrasunicas:
		caracteristicas['%s' % palavras] = (palavras in doc)
	return caracteristicas

def addDataBase(string, method, genre):
	a=0
	manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','r', encoding="utf8")
	for line in manipulador.readlines():
		if line.split(',')[0] == string:
			a=1
	if a ==0:
		manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','a', encoding="utf8")
		manipulador.write('\n' + string + ',' + method +',' + genre)
		manipulador.close()

#endregion

#region CleanString

def getMusicName(string):
	off_words = ['spotify', 'música', 'youtube', 'vídeo']
	return cleanString(off_words,string)

def getMessage(string):
	txt = string.split('que',1)
	msg = txt[1]
	off_words = ['dizendo', 'mensagem', 'falando', 'responde', 'para', 'pro','pra']	
	return (cleanString(off_words,txt[0]).replace("amorzinho","mozinho"), msg)

def getProduct(string):
	off_words = ['custa', 'preço', 'menor', 'melhor', 'valor']
	return cleanString(off_words,string)

def getFile(string):
	off_words = ['arquivo', 'cópias', 'programa','imprimir']
	return cleanString(off_words,string).strip()

def cleanStringGen(string):
	off_words = {'pesquisa','procura', 'vê','vê', 'me fala', 'fala', 'me fala','busca','acha','me diz'}
	sub = {'um':'1','uma':'1', 'dois':'2', 'duas': '2', 'mateus':'matheus'}
	for word in string.split():
		if word in sub:
			string = string.replace(word,sub[word]) 
	for p in off_words:
		if string.startswith(p):
			string = string.replace(p,'',1)
			break
	if ' para mim' in string:
		string = string.replace(' para mim','',1)
	return string.strip()

def cleanString(off_words, string):
	temp = string.split()
	del (temp[0])
	name =''
	for p in temp:
		if p not in stopwords and p not in off_words:
			name+=p +' '
	return name.strip()

#endregion

#region SystemOp


def windowsSearch(string):
	pyautogui.press('win')
	pyautogui.write(unidecode.unidecode(string))
	pyautogui.press('enter')

def openProgram(string):
	windowsSearch(getFile(string))
		
def printFile(string):
	temp = getFile(string)
	t = temp.split()
	try:
		n = int(t[0].replace('duas','2'))
		del (t[0])
		temp = ''
		for word in t:
			temp += " " + word
		
	except:
		n =1
	windowsSearch(temp)
	time.sleep(6)
	for i in range(n):
		pyautogui.press('enter')
		time.sleep(1)
		pyautogui.hotkey('ctrl', 'p')
		pyautogui.press('enter')
		time.sleep(3)
	pyautogui.hotkey('alt', 'f4')

def shutdownPC(string):
	os.system('shutdown -s')

#endregion

#region GoogleOp

def getGoogleUrl(string):
	browser.get('http://www.google.com')
	elementoEntrada = browser.find_element_by_css_selector('.gLFyf.gsfi') # procura o elemento
	elementoEntrada.send_keys(string) # preenche 
	elementoEntrada.submit() # realiza a pesquisa
	return browser.current_url

def posTeam(string):
	req = Request(googleSearch(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	time = soup.find('div', class_='ofy7ae').get_text()
	a = soup.find_all('span', class_ = 'ellipsisize hsKSJe')
	indice =0
	for i, temp in enumerate (a):
		if temp.get_text() in time:
			indice =i
	a = soup.find_all('div', class_='iU5t0d')

	speak("O " + time + " está na " + a[indice].get_text() + "ª posição")

def convertValue(string):
	off_words = {'mais', 'menos','soma','subtrai','elevado','logaritmo','raiz','vezes','multiplicado','dividido','%','porcento','x','fatorial','divide','sobre','exponencial', '+', '-','/'}
	for p in string.split():
		if p in off_words:
			solveCalc(string)
			return		
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	values = []
	units = []
	try:
		for value in soup.find_all('input', class_='vXQmIe gsrt'):
			values.append(value['value'])
		for unit in soup.find_all('select', class_='OR9QXc LNn04b gsrt'):
			units.append(unit.find('option', selected = '1').get_text())
		if values == []:
			values.append(soup.find('input', class_='ZEB7Fb vk_gy vk_sh Hg3mWc')['value'])
			values.append(soup.find('input', class_='a61j6 vk_gy vk_sh Hg3mWc')['value'])
			unit = soup.find('select', class_='l84FKc R9zNe vk_bk Uekwlc')
			units.append(unit.find('option', selected = '1').get_text())
			unit = soup.find('select', class_='NKvwhd R9zNe vk_bk Uekwlc')
			units.append(unit.find('option', selected = '1').get_text())
		speak(values[0] + " " + units[0] +' equivalem a ' + values[1] + " " + units[1])
	except:
		googleSearch(string)

def solveCalc(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	try:
		resp = soup.find('span', class_='qv3Wpe').get_text()
		speak(round(float(resp), 3))			
	except:
		googleSearch(string)

def temperature(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	try:
		if 'chuva' in string or 'chover' in string :
			speak("A chance de chuva é de: " + soup.find('span', id='wob_pp').get_text())
		else:
			temp = soup.find('span', id='wob_tm').get_text()
			local = soup.find('div', id='wob_loc').get_text()
			if 'hoje' in string or 'agora' in string or 'fazendo' in string or'esta' in string or'atual' in string:
				speak("Fazem " + temp + "° Celsius em " + local)
				
			else:
				speak("A previsão do tempo para " + local + "é de " + temp +"° Celsius")
	except:
		googleSearch(string)

def locate(string):
	googleSearch(string)

def findPrice(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	inicio = time.time()
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	if 'ações' in string or 'ação' in string:
		stockValue(string)
	else:
		try:
			adverts = soup.find_all('div', class_='mnr-c pla-unit')
			bestPrice = 0
			bestMarket = ''
			prod = getProduct(string)
			for ad in adverts:
				price = int(re.sub('[^0-9]', '', ad.find('div', class_='qptdjc').get_text()))/100
				name = ad.find('div', class_='r4awE').get_text().lower()
				if prod in name and (price < bestPrice or bestPrice ==0):
					bestPrice = price
					bestMarket = ad.find('span',class_='a LnPkof').get_text()
			fim= time.time()
			print(fim-inicio)
			speak ("O menor preço de " + prod[0] + " " + prod[1] + " encontrado foi " + re.sub(r'\.',',',str (bestPrice)) + " reais em " +bestMarket)
		except:
			googleSearch(string)

def nextMatch(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")

	times = soup.find_all('div', class_="ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx")
	jogo = []
	for time in times:
		jogo.append(time.find('span').string)
	temp = ('o próximo jogo é: ' + jogo[0] + 'contra ' + jogo[1])
	speak(temp)

def googleSearch(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	try:
		resp = soup.find('div', class_='Z0LcW XcVN5d').get_text()
		if not any(char.isdigit() for char in resp):
			try:
				resp = soup.find('span', class_='hgKElc').get_text()
			except:
				print ('a')
	except:
		try:
			temp = soup.find('div', class_='kno-rdesc')
			resp = temp.find('span').get_text()
		except:
			try:
				resp = soup.find('div', class_='Z0LcW XcVN5d AZCkJd').get_text()
			except:
				try:
					resp = soup.find('span', class_='hgKElc').get_text()
				except:
					try:
						resp = soup.find('ul', class_='i8Z77e').get_text()
					except:
						try:
							resp = soup.find('ol', class_='X5LH0c').get_text()
						except:
							try:
								resp = soup.find('span', class_='desktop-title-subcontent').get_text()
							except:
								#resp = soup.find('span', class_='aCOpRe').get_text()
								resp = "Desculpe, não achei nada relacionado"
	speak (re.sub(r'\([^)]*\)', '', resp))

def stockValue(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	try:
		resp = soup.find_all('span', class_="IsqQVc NprOob XcVN5d")
		valor = resp[0].get_text()
		resp = soup.find_all('span', class_="WlRRw IsqQVc fw-price-dn")
		if resp == []:
			resp = soup.find_all('span', class_="WlRRw IsqQVc fw-price-up")
		variation = resp[0].find_all('span')[1]['aria-label']
		speak ("o valor desta ação é de: " + valor + " reais, e " + variation)
	except:
		googleSearch(string)

#endregion

#region Schedule

def convertDate(string):
	off_words = {'agenda','calendário'}
	day = 0
	month = 0
	year = 0
	hour = ''
	sd = 0
	ed = 0
	sh = 0
	eh = 0
	months = {'janeiro':'1','fevereiro':'2','março':'3','abril':'4','maio':'5','junho':'6','julho':'7','agosto':'8','setembro':'9','outubro':'10','novembro':'11','dezembro':'12'}
	temp = string.split()
	del(temp[0])
	for i, word in enumerate (temp):
		if word == 'dia' and temp[i+1].isdigit():
			sd = i
			day = temp[i+1]
			if i == len(temp)-2 or temp[i+2] == 'às' or temp[i+2].isdigit():
				month = datetime.today().month
				year = datetime.today().year
				ed = i+1
			else:
				ed = i+3
				if temp[i+3].isdigit():
					month = temp[i+3]
				else:
					month = months[temp[i+3]]
				if len(temp)> i+4:
					if temp[i+4] == 'de' and temp[i+5].isdigit():
						year= temp[i+5]
						ed = i+5
				if year ==0:
					year = datetime.today().year			
		if (word == 'às' or word=='das' or word =='umas') and temp[i+1].isdigit():
			sh = i
			hour = temp[i+1]
			if temp[i+2] == 'e':
					hour+=':' + temp[i+3]
					eh = i+3
			else:
				hour += ':00'
				eh = i+1
		if word == 'horas' and hour == '':
			if temp[i-1].isdigit():
				hour = temp[i-1]+ ':00'
				eh = i
		if word.isdigit() and hour ==  '':
			if temp[i+1] == 'e' and (temp[i+2].isdigit() or temp[i+2] == 'meia'):
				hour = word
				hour+=':' + temp[i+2]
				sh = i
				eh = i+2
		hour = hour.replace('meia','30')
		
	if len(temp)-1> eh:
		if temp[eh+1]=='horas': 
			eh += 1
	if sd < sh:
		sh=sd
	if ed > eh:
		eh = ed
	eventName='teste '
	for i, word in enumerate (temp):
		if 	i<sh  or i > eh:
			eventName+=word + ' '
	a = str(year) + '-' + str(month) + '-' + str(day) + 'T' +hour + ":00"
	return cleanString(off_words, eventName) , a

def checkSchedule(string):
	# Call the Calendar API
	now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	service = authCalendar()
	events_result = service.events().list(calendarId='primary', timeMin=now,
										maxResults=10, singleEvents=True,
										orderBy='startTime').execute()
	events = events_result.get('items', [])

	if not events:
		speak('Nenhum evento próximo')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		speak(event['summary'])

def authCalendar():
	SCOPES = ['https://www.googleapis.com/auth/calendar']
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(req())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('calendar', 'v3', credentials=creds)
	return service

def addEvent(string):
	info = convertDate(string)
	event = {
	'summary': info[0],
	'location': '',
	'start': {
		'dateTime': info[1],
		'timeZone': 'America/Sao_Paulo',
	},
	'end': {
		'dateTime': info[1],
		'timeZone': 'America/Sao_Paulo',
	}
	}
	service = authCalendar()
	event = service.events().insert(calendarId='primary', body=event).execute()
	print ('Event created: %s' % (event.get('htmlLink')))

#endregion

#region OtherFunctions

def checkGmail(string):
	n = 5
	for char in string.replace('dois','2'):
		if char.isdigit():
			n = int(char)
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
		for i, message in enumerate(messages):
			if i == n:
				break
			msg = service.users().messages().get(userId='me', id=message['id']).execute()
			for temp in msg['payload'].get('headers'):
				if 'From' in temp.get('name'):
					a=temp.get('value').split('<')
					speak ('Email de: '+a[0])
			speak (msg['snippet'])

def spotifySearch(string):
	music = getMusicName(string)
	options_temp = webdriver.ChromeOptions() 
	options_temp.add_argument('user-data-dir=C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\dataChrome\\UserData')
	options_temp.add_argument('--profile-directory=Profile 2')
	browser_temp = webdriver.Chrome(executable_path='C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\dataChrome\\chromedriver', options=options_temp)
	browser_temp.get('https://open.spotify.com/search')
	if 'músicas' in music or 'playlist' in music or 'favoritas' in music:
		ui.WebDriverWait(browser_temp, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ac0df040748287f39652cc42e3b762ba-scss']"))).click()
		ui.WebDriverWait(browser_temp, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[3]/div/button"))).click()
	else:
		ui.WebDriverWait(browser_temp, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='_748c0c69da51ad6d4fc04c047806cd4d-scss']"))).send_keys(music)
		ui.WebDriverWait(browser_temp, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_9811afda86f707ead7da1d12f4dd2d3e-scss']"))).click()
		time.sleep(3)
	temp = browser_temp.find_elements_by_xpath("//div[@class='playback-bar__progress-time _5f899d811cf206c5925f6450626fb0aa-scss']")
	n = temp[1].get_attribute("innerHTML")
	temp = n.split(':')
	time.sleep(int(temp[0])*60 + int(temp[1]))
	browser_temp.quit()
	
def youtubeSearch(string):	
	browser_temp = webdriver.Chrome(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\\dataChrome\\chromedriver')
	browser_temp.get('https://www.google.com.br/videohp?hl=pt-BR')
	elementoEntrada = browser_temp.find_element_by_class_name('lst.tiah') # procura o elemento
	elementoEntrada.send_keys(getMusicName(string)) # preenche com a palavra amazonia
	elementoEntrada.submit()
	ui.WebDriverWait(browser_temp, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='rGhul IHSDrd']"))).click()
	try:
		time.sleep(6)
		ui.WebDriverWait(browser_temp, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']"))).click()
	except:
		print("")
	finally:
		n = browser_temp.find_element_by_class_name('ytp-time-duration').get_attribute("innerHTML")
		temp = n.split(':')
		time.sleep(int(temp[0])*60 + int(temp[1]))
		browser.quit()

def whatsAppSend(string):
	content = getMessage(string)
	options = webdriver.ChromeOptions() 
	options.add_argument('user-data-dir=C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\UserData')
	options.add_argument('--profile-directory=Profile 2')
	browser = webdriver.Chrome(executable_path='C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\chromedriver', options=options)
	browser.get('https://web.whatsapp.com/')
	ui.WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_1awRl copyable-text selectable-text'][@data-tab='3']"))).send_keys(content[0])
	ui.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='matched-text _1VzZY']"))).click()
	ui.WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_1awRl copyable-text selectable-text'][@data-tab='6']"))).send_keys(content[1])
	ui.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_2Ujuu']"))).click()	



#endregion

#region ExternalFunctions

def nodeSimpleRequest(string):
	requests.get('http://192.168.0.25/genericArgs?command='+string)

def nodeCompostRequest(string):
	requests.get('http://192.168.0.25/genericArgs?command=e&txt='+string+'/')

def lightOn(string):
	nodeSimpleRequest('a')
	
def lightOff(string):
	nodeSimpleRequest('f')

def speakerPower(string):
	nodeSimpleRequest('c')

def speakerLine(string):
	nodeSimpleRequest('l')

def speakerBlue(string):
	nodeSimpleRequest('b')

def netPower(string):
	nodeSimpleRequest('n')

def tvPower(string):
	nodeSimpleRequest('t')

def changeChannelTv(string):
	changeSourceTv(3)
	off_words = {'tv','canal','televisão'}
	canal = cleanString(off_words,string)
	sub = {'globo':'501','sbt':'509','band':'505','bandeirantes':'505','gazeta':'521', 'rede tv':'508','record':'519','sbn':'188','jimmy':'188'}
	for word in canal.split():
		if word in sub:
			canal = canal.replace(word,sub[word]) 	
	nodeCompostRequest(canal)

def showProgramTv(string):
	nodeSimpleRequest('p')
	time.sleep(10)
	nodeSimpleRequest('v')

def searchTitleTv(string):
	off_words = {'tv','televisão','série','filme','desenho'}
	client = getTvClient()
	time.sleep(1)
	nodeSimpleRequest('s')
	time.sleep(3)
	inp = InputControl(client)
	inp.connect_input()
	inp.type(cleanString(off_words,string))
	time.sleep(1)            # This sends keystrokes, but needs the keyboard to                                                  # be displayed on the screen.
	inp.enter()
	inp.ok()
	time.sleep(8)
	inp.ok()


def openAppTv(string):
	client = getTvClient()
	off_words = {'plus', 'tv', 'pra mim'}   
	app = ApplicationControl(client)
	apps = app.list_apps()  
	yt = [x for x in apps if cleanString(off_words,string) in x["title"].lower()][0]
	launch_info = app.launch(yt)                         
	inp = InputControl(client)           
	time.sleep(15)                                                  
	inp.enter()  	

def getTvClient():
	store = {'client_key': 'd123747cbbfa54a322dad4343163f646'}
	while True:
		try:
			client = WebOSClient("192.168.0.22")
			client.connect()
			for status in client.register(store):
				if status == WebOSClient.PROMPTED:
					print("Please accept the connect on the TV!")
				elif status == WebOSClient.REGISTERED:
					print("Registration successful!")
					return client
		except:
			tvPower('a')
			time.sleep(2)

def changeSourceTv(a):
    client = getTvClient()
    source_control = SourceControl(client)
    source_control.set_source(source_control.list_sources()[a])

def conTv(string):
	changeSourceTv(2)
	os.system('DisplaySwitch.exe /external')

def desconTv(string):
	os.system('DisplaySwitch.exe /extend')
	
def powerOffAll(string):
	netPower(string)
	tvPower(string)
	speakerPower(string)
	lightOff(string)
	shutdownPC(string)
	
#endregion

#region MediaControl

sensimedia = 6
def upMedia(string):
	for i in range (sensimedia):
		pyautogui.press('volumeup')
def downMedia(string):
	for i in range (sensimedia):
		pyautogui.press('volumedown')
def muteMedia(string):
	pyautogui.press('volumemute')
def nextMedia(string):
	pyautogui.press('nexttrack')
def backMedia(string):
	pyautogui.press('prevtrack')
	pyautogui.press('prevtrack')
def repeatMedia(string):
	pyautogui.press('prevtrack')
def playMedia(string):
	pyautogui.press('playpause')

def upMediaTv(string):
	client = getTvClient()	
	media = MediaControl(client)
	for i in range (sensimedia*2):
		media.volume_up()          

def downMediaTv(string):
	client = getTvClient()
	media = MediaControl(client)
	for i in range (sensimedia*2):
		media.volume_up()  	
def upMediaNet(string):
	for i in range (int(sensimedia/2)):
		nodeSimpleRequest('>')
def downMediaNet(string):
	for i in range (int(sensimedia/2)):
		nodeSimpleRequest('<')
def upMediaSpeaker(string):
	for i in range (int(sensimedia/2)):
		nodeSimpleRequest('+')
def downMediaSpeaker(string):
	for i in range (int(sensimedia/2)):
		nodeSimpleRequest('-')
#endregion

#region MainFunctions

def startMethod(string):	
	for phrase in string.split(" e "):
		genre = classify(classgenre,phrase)
		if genre != 'whatsAppOp':
			phrase = cleanStringGen(phrase)
		method = classify(training(genre),phrase)
		print(method)	
		speak('ok')
		exec(method + "('"+ phrase + "')")
		addDataBase(phrase,method,genre)
		time.sleep(2)

def speak(text):
	speaker = pyttsx3.init()
	speaker.setProperty('voice', 'pt-Brasil')
	speaker.setProperty('rate', 150) 
	speaker.say(text)
	speaker.runAndWait()

def listen():
	r = sr.Recognizer()
	with sr.Microphone() as s:	
		while True:
			r.adjust_for_ambient_noise(s)
			inicio = time.time()
			audio = r.listen(s)
			try:
				inicio = time.time()			
				speech = r.recognize_google(audio, language='pt').lower()
				fim = time.time()
				print(fim-inicio)
				print(speech)
				return speech
			except:
				print('a')	

#endregion

#region GlobalIntances

options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\dataChrome\chromedriver', options=options)

stopwords=nltk.corpus.stopwords.words('portuguese')
stemmer = nltk.stem.RSLPStemmer()
classgenre =  training('')

#endregion

#region Program

while True:
	speech = listen()
	speech = speech.replace('maia','maya',1)
	if 'maya' in speech:
		if len(speech.split())<3:
			speak('sim')
			speech = listen()
		_thread.start_new_thread(startMethod, (speech.replace('Maya ',"",1),))

#endregion