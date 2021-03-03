total = 0
atual = 10
cont = 0 
for i in range(6):
	for j in range(6):
		if atual >= 210:
			if (cont <1):	
				total += atual
			else:
				total += atual/2
			cont +=1
		atual +=10	
print (total-1500)
print (atual)
print(cont)