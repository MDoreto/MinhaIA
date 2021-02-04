import nltk
import time
stopwords=nltk.corpus.stopwords.words('portuguese')
manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','r', encoding="utf8")

base = []
stemmer = nltk.stem.RSLPStemmer()


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


for line in manipulador.readlines():
	temp = line.rstrip('\n').split(',')
	t = (temp[0].lower(),temp[2])
	base.append(t)
manipulador.close()
frasescomstemming = fazstemmer(base)
frequencia = buscafrequencia(buscapalavras(frasescomstemming))
palavrasunicas = busca_palavrasunicas(frequencia)
basecompleta = nltk.classify.apply_features(extrai_palavras,frasescomstemming)
classificador = nltk.NaiveBayesClassifier.train(basecompleta) 
metho =''
genre = ''
def machine (speech,base):
	testestem = []
	for (palavras) in speech.split():
		comstem = [p for p in palavras.split()]
		testestem.append(str(stemmer.stem(comstem[0])))
	nova_frase = extrai_palavras(testestem)		
	distribuicao = classificador.prob_classify(nova_frase)
	method = ['',0]
	
	for classe in distribuicao.samples():
		a=0
		for(frase,genero) in base:
			if genero == classe:
				a+= 1
		print(classe)
		print(a)
		print(distribuicao.prob(classe))
		if distribuicao.prob(classe) > method[1] and distribuicao.prob(classe) > 0.3:
			genre = classe
			method[1] = distribuicao.prob(classe)
	print("____________________________________________________")
	print("____________________________________________________")
	print("____________________________________________________")
	base = []

	manipulador = open(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\database.txt','r', encoding="utf8")
	for lines in manipulador.readlines():
		temp = lines.rstrip('\n').split(',')
		if (temp[2] == genre):
			t = (temp[0].lower(),temp[1])
			base.append(t)
	manipulador.close()
	frasescomstemming = fazstemmer(base)
	frequencia = buscafrequencia(buscapalavras(frasescomstemming))
	palavrasunicas = busca_palavrasunicas(frequencia)
	basecompleta = nltk.classify.apply_features(extrai_palavras,frasescomstemming)
	temp_classificador = nltk.NaiveBayesClassifier.train(basecompleta) 
	manipulador.close
	nova_frase = extrai_palavras(testestem)		
	distribuicao = temp_classificador.prob_classify(nova_frase)
	method = ['',0]
	for classe in distribuicao.samples():
		print(classe)
		print(distribuicao.prob(classe))
		if distribuicao.prob(classe) > method[1]:
			method[0] = classe
			method[1] = distribuicao.prob(classe)
	print('------------MÉTODO ESCOLHIDO---------------')
	print(method[0])
speech = 'mostra a programação da tv'
inicio = time.time()
machine(speech,base)
fim = time.time()
print('------------TIME---------------')
print(fim-inicio)

