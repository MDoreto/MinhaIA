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
	return (results[0][0] + "\\" + results[0][1])

def printFile(string):
	n=1
	for i in range (int(n)):
		win32api.ShellExecute (0,"print",findFiles(getFile(string),1),n,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
		time.sleep(10)	