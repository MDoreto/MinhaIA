from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen  
import time
import nltk
stopwords=nltk.corpus.stopwords.words('portuguese')
#options = webdriver.ChromeOptions()
#options.add_argument("--headless")
#browser = webdriver.Chrome(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis/chromedriver', options=options)
def getMusicName(string):
	off_words = ['spotify', 'música', 'youtube', 'vídeo']
	return cleanString(off_words,string)

def cleanString(off_words, string):
	temp = string.split()
	del (temp[0])
	name =''
	for p in temp:
		if p not in stopwords and p not in off_words:
			name+=p +' '
	return name.strip()

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

def getGoogleUrl(string):
	browser.get('http://www.google.com')
	elementoEntrada = browser.find_element_by_css_selector('.gLFyf.gsfi') # procura o elemento
	elementoEntrada.send_keys(string) # preenche 
	elementoEntrada.submit() # realiza a pesquisa
	return browser.current_url

def spotifySearch(string):
	music = getMusicName(string)
	options_temp = webdriver.ChromeOptions() 
	options_temp.add_argument('user-data-dir=C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\UserData')
	options_temp.add_argument('--profile-directory=Profile 2')
	browser_temp = webdriver.Chrome(executable_path='C:\\Users\\mathe\\OneDrive\\Área de Trabalho\\jarvis\\chromedriver', options=options_temp)
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

def solveCalc(string):
	req = Request(getGoogleUrl(string), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	response = urlopen(req).read()
	soup = BeautifulSoup(response, "html.parser")
	try:
		resp = soup.find('span', class_='qv3Wpe').get_text()
		print(round(float(resp), 3))
			
	except:
		googleSearch(string)

spotifySearch('toca a minha playlist')