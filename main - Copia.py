import time
import os
import json
import speech_recognition as sr
import pyttsx3
import http.client
import tempfile
import win32api
import win32print
import win32com.client
import pyautogui
from urllib.request import Request, urlopen  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
import nltk
import unidecode
from pywebostv.discovery import *    # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *
import time


r = sr.Recognizer()


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

def addDataBase(string, function):
    a=0
    for (text, classe) in base:
        if text == string:
            a=1
    if a ==0:
        manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','a', encoding="utf8")
        manipulador.write('\n' + string + ',' + function)


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

def cleanString(off_words, string):
	temp = string.split()
	del (temp[0])
	name =''
	for p in temp:
		if p not in stopwords and p not in off_words:
			name+=p +' '
	return name.strip()

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


def openAppTv(string):

	store = {'client_key': 'd123747cbbfa54a322dad4343163f646'}


	# Scans the current network to discover TV. Avoid [0] in real code. If you already know the IP,
	# you could skip the slow scan and # instead simply say:
	client = WebOSClient("192.168.0.22")
	client.connect()
	for status in client.register(store):
		if status == WebOSClient.PROMPTED:
			print("Please accept the connect on the TV!")
		elif status == WebOSClient.REGISTERED:
			print("Registration successful!")
	off_words = {'plus', 'tv', 'pra mim'}
	# Keep the 'store' object because it contains now the access token
	# and use it next time you want to register on the TV.
	print (cleanString(off_words,string))   # {'client_key': 'ACCESS_TOKEN_FROM_TV'}
	app = ApplicationControl(client)
	apps = app.list_apps()  
	yt = [x for x in apps if cleanString(off_words,string) in x["title"].lower()][0]
													# Search for YouTube & launch it (Of course, don't
													# be this lazy. Check for errors). Also, Try
													# searching similarly for "amazon", "netflix" etc.
	launch_info = app.launch(yt)                         

	inp = InputControl(client)           # This sends keystrokes, but needs the keyboard to
	time.sleep(15)                                                  # be displayed on the screen.
	inp.enter()  

def getGoogleUrl(string):

	browser = webdriver.Chrome(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis/chromedriver')
	browser.get('http://www.google.com')
	elementoEntrada = browser.find_element_by_css_selector('.gLFyf.gsfi') # procura o elemento
	elementoEntrada.send_keys(string) # preenche com a palavra amazonia
	elementoEntrada.submit() # realiza a pesquisa

	return browser.current_url

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
	resp = soup.find('span', class_='hgKElc').get_text()
	speak (re.sub(r'\([^)]*\)', '', resp))

def stockValue(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	resp = soup.find_all('span', class_="IsqQVc NprOob XcVN5d")
	valor = resp[0].get_text()
	resp = soup.find_all('span', class_="WlRRw IsqQVc fw-price-dn")
	if resp == []:
		resp = soup.find_all('span', class_="WlRRw IsqQVc fw-price-up")
	variation = resp[0].find_all('span')[1]['aria-label']
	speak ("o valor desta ação é de: " + valor + " reais, e " + variation)
	
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

def speak(text):
	speaker = pyttsx3.init()
	speaker.setProperty('voice', 'brazil')
	speaker.setProperty('rate', 150) 
	speaker.say(text)
	speaker.runAndWait()

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

def temperature(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")

	if 'chuva' in string or 'chover' in string :
		speak("A chance de chuva é de: " + soup.find('span', id='wob_pp').get_text())
	else:
		temp = soup.find('span', id='wob_tm').get_text()
		local = soup.find('div', id='wob_loc').get_text()
		if 'hoje' in string or 'agora' in string or 'fazendo' in string or'esta' in string or'atual' in string:
			speak("Fazem " + temp + "° Celsius em " + local)
			
		else:
			speak("A previsão do tempo para " + local + "é de " + temp +"° Celsius")

def locate(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	try:
		cap = soup.find('div', class_='HwtpBd gsrt PZPZlf').get_text()
	except:
		cap = soup.find('span', class_='desktop-title-subcontent').get_text()
	speak (cap)

def findPrice(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	adverts = soup.find_all('div', class_='mnr-c pla-unit')
	bestPrice = 9999999999
	bestMarket = ''
	prod = getProduct(string)
	for ad in adverts:
		price = int(re.sub('[^0-9]', '', ad.find('div', class_='qptdjc').get_text()))/100
		name = ad.find('div', class_='r4awE').get_text().lower()
		if prod in name and price < bestPrice:
			bestPrice = price
			bestMarket = ad.find('span',class_='a LnPkof').get_text()
	speak ("O menor preço de " + prod[0] + " " + prod[1] + " encontrado foi " + re.sub(r'\.',',',str (bestPrice)) + " reais em " +bestMarket)

def spotifySearch(string):
	options = webdriver.ChromeOptions() 
	options.add_argument('user-data-dir=C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\UserData')
	options.add_argument('--profile-directory=Profile 2')
	browser = webdriver.Chrome(executable_path='C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\chromedriver', options=options)
	browser.get('https://open.spotify.com/search')
	ui.WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='_748c0c69da51ad6d4fc04c047806cd4d-scss']"))).send_keys(getMusicName(string))
	ui.WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_9811afda86f707ead7da1d12f4dd2d3e-scss']"))).click()

def youtubeSearch(string):
	browser = webdriver.Chrome(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis/chromedriver')
	browser.get('https://www.google.com.br/videohp?hl=pt-BR')
	elementoEntrada = browser.find_element_by_class_name('lst.tiah') # procura o elemento
	elementoEntrada.send_keys(getMusicName(string)) # preenche com a palavra amazonia
	elementoEntrada.submit()
	ui.WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='rGhul IHSDrd']"))).click()

	try:
		time.sleep(6)
		ui.WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']"))).click()
	except:
		print("")

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


stopwords=nltk.corpus.stopwords.words('portuguese')
manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','r', encoding="utf8")
base = []
testestem = []
stemmer = nltk.stem.RSLPStemmer()

for line in manipulador.readlines():
	temp = line.rstrip('\n').split(',')
	t = (temp[0].lower(),temp[1])
	base.append(t)
frasescomstemming = fazstemmer(base)
frequencia = buscafrequencia(buscapalavras(frasescomstemming))
palavrasunicas = busca_palavrasunicas(frequencia)
basecompleta = nltk.classify.apply_features(extrai_palavras,frasescomstemming)
classificador = nltk.NaiveBayesClassifier.train(basecompleta) 

with sr.Microphone() as s:			
	r.adjust_for_ambient_noise(s)
	while True:
		#try:
			audio = r.listen(s)
			speech = r.recognize_google(audio, language='pt')
			speech = speech.lower()
			speech = speech.replace('mateus', 'matheus')
			print(speech)								
			if 'volume' in speech:
				sens =5
				if 'aumenta' in speech:
					for i in range(sens):
						pyautogui.press('volumeup') 
				if 'diminui' in speech or 'abaixa' in speech:
					for i in range(sens):
						pyautogui.press('volumedown') 
				if 'tira' in speech or 'muta' in speech:
					for i in range(sens):
						pyautogui.press('volumemute')
			else: 
				for (palavras) in speech.split():
					comstem = [p for p in palavras.split()]
					testestem.append(str(stemmer.stem(comstem[0])))
				nova_frase = extrai_palavras(testestem)			
				distribuicao = classificador.prob_classify(nova_frase)
				method = ['',0]
				for classe in distribuicao.samples():
					if distribuicao.prob(classe) > method[1] and distribuicao.prob(classe) > 0.3:
						method[0] = classe
						method[1] = distribuicao.prob(classe)
				print(method[0] + r"('"+ speech + r"')")	
				exec(method[0] + "('"+ speech + "')")
				addDataBase(speech,method[0])	
		#except:
		#	speak('Não entendi')