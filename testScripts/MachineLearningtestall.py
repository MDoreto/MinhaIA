import nltk;
import time;
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

def startMethod(string):	
	genre = classify(classgenre,string)
	if genre != 'whatsAppOp':
		string = cleanStringGen(string)
	method = classify(training(genre),string)
	return method
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
	
stopwords=nltk.corpus.stopwords.words('portuguese')
stemmer = nltk.stem.RSLPStemmer()
total = 0
timetotal = 0
classgenre =  training('')
manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\testScripts\database.txt','r', encoding="utf8")
acerto = 0
"""frase = 'marcar na calendário 15 e meia dia 4 de junho festa de casamento'
print (startMethod(frase))"""
for lines in manipulador.readlines():
	temp = lines.rstrip('\n').split(',')
	temptime = time.time()
	a = startMethod(temp[0])
	timetotal +=(time.time()-temptime)
	total +=1 
	if  (a ==temp[1]):
		acerto+= 1
	else:
		print(temp[0] +  " encontrado: " + a + " esperado: " + temp[1])

print((acerto/total)*100)
print(timetotal/total)
