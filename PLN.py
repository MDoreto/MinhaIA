from google.cloud import language_v1
import time
import nltk
stopwords=nltk.corpus.stopwords.words('portuguese')
def sample_analyze_syntax(text_content):
	"""
	Analyzing Syntax in a String

	Args:
	  text_content The text content to analyze
	"""

	client = language_v1.LanguageServiceClient.from_service_account_json(r'C:\Users\mathe\OneDrive\Área de Trabalho\jarvis\cred.json')

	# text_content = 'This is a short sentence.'

	# Available types: PLAIN_TEXT, HTML
	type_ = language_v1.Document.Type.PLAIN_TEXT

	# Optional. If not specified, the language is automatically detected.
	# For list of supported languages:
	# https://cloud.google.com/natural-language/docs/languages
	language = "pt-br"
	document = {"content": text_content, "type_": type_, "language": language}

	# Available values: NONE, UTF8, UTF16, UTF32
	encoding_type = language_v1.EncodingType.UTF8

	response = client.analyze_syntax(request = {'document': document, 'encoding_type': encoding_type})
	# Loop through tokens returned from the API
	for token in response.tokens:
		print(u"Lemma: {}".format(token.lemma))
		# Get the text content of this token. Usually a word or punctuation.
		text = token.text
		print(u"Token text: {}".format(text.content))
		#print(
		#	u"Location of this token in overall document: {}".format(text.begin_offset)
		#)
		# Get the part of speech information for this token.
		# Parts of spech are as defined in:
		# http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
		part_of_speech = token.part_of_speech
		# Get the tag, e.g. NOUN, ADJ for Adjective, et al.
		print(
			u"Part of Speech tag: {}".format(
				language_v1.PartOfSpeech.Tag(part_of_speech.tag).name
			)
		)
		# Get the voice, e.g. ACTIVE or PASSIVE
		#print(u"Voice: {}".format(language_v1.PartOfSpeech.Voice(part_of_speech.voice).name))
		# Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
		#print(u"Tense: {}".format(language_v1.PartOfSpeech.Tense(part_of_speech.tense).name))
		# See API reference for additional Part of Speech information available
		# Get the lemma of the token. Wikipedia lemma description
		# https://en.wikipedia.org/wiki/Lemma_(morphology)
		print(u"Lemma: {}".format(token.lemma))
		# Get the dependency tree parse information for this token.
		# For more information on dependency labels:
		# http://www.aclweb.org/anthology/P13-2017
		dependency_edge = token.dependency_edge
		#
		# 
		# print(u"Head token index: {}".format(dependency_edge.head_token_index))
		print(
			u"Label: {}".format(language_v1.DependencyEdge.Label(dependency_edge.label).name)
		)

	# Get the language of the text, which will be the same as
	# the language specified in the request or, if not specified,
	# the automatically-detected language.
	print(u"Language of the text: {}".format(response.language))

def getMusicName(string):
	off_words = ['spotify', 'música', 'youtube', 'vídeo']
	return cleanString(off_words,string)

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

off_words = {'tv','televisão','série','filme','desenho'}
inicio = time.time()
print(getMusicName(cleanStringGen("Toca minhas músicas favoritas")))
fim = time.time()
print(fim-inicio)
