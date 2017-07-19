import socket
import time
import hashlib
import struct
import os
import collections

dicionario = {}
ordemEntrada = []
conjuntoRefTerm = set()
determEncontrados = set()


########################################### Funções ###########################################
# ordered dict
def read_entrada(nome):
	arquivo  = open('arquivos/'+nome, "rb")
	arquivo.seek(0)
	entrada  = arquivo.read().decode()
	# x = f.read().decode()
	return entrada

def separaGramaticaDeTokens(tipo, entrada):	
	entrada = str(entrada).replace(" ","")
	entrada   = entrada.split('\n')
	gram = ''
	tok  = ''
	for i in entrada:
		if i.find("<") == 0: # gramatica
			gram = str(gram)+str(i)+'\n'
		else:			# token
			tok = str(tok)+str(i)+'\n'

	if tipo == 0:
		return gram
	else:
		return tok


##### Tokens #####
def cria_automatoTok(lista):
	global ordemEntrada
	# print("lista tokens")
	# print(lista)
	# lista = lista.replace(" ","")
	lista = lista.split("\n")
	# print(lista)
	# print("final tokens")
	for i in lista:
		if i != '':	    # cada token
			cont = 0
			for j in i: # cada caractere do token
				if cont == 0: # primeiro caracterer do token
					# print("gamb")
					# print(dicionario)
					if dicionario == {}:
						# print('Dicionario novo')
						dicionario['S'] = [0, {j:''}]
						ordemEntrada.append('S')
						# print(dicionario)

					if j in dicionario['S'][1]: # encontrou o caractere do token
						# print("if")
						estadoFinal = buscaProxEstado(j)

						dicionario['S'][1][j] = str(dicionario['S'][1][j])+str(estadoFinal)
						# print(dicionario['S'][1])
					else:
						# print("else")
						estadoFinal = buscaProxEstado(j)
						dicionario['S'][1][j] = estadoFinal
						#print(dicionario['S'][1]['s'])
				else: # gera um novo estado...
					# print("else2")
					proximoEstado = ordemEntrada[len(ordemEntrada)-1]
					# print("novo estado")
					# print(proximoEstado)
					estadoFinal = buscaProxEstado(j)
					dicionario[proximoEstado] = [0, {j:estadoFinal}]
					dicionario[proximoEstado][1][j] = ordemEntrada[len(ordemEntrada)-1]
				
				# Valida se é estado final ou não
				if cont == len(i)-1: # ultima letra do token... gera um estado final
					dicionario[estadoFinal] = [1, {'':''}]


				# print(dicionario)

				cont += 1
				#print(j)
	
	# print("Dicionario")
	# print(dicionario)
	# print("Terminais")
	# print(conjuntoRefTerm)
	# print("Nao terminais")
	# print(ordemEntrada)

def buscaProxEstado(terminal):
	global ordemEntrada, conjuntoRefTerm
	# if len(ordemEntrada) > 0:
	ultimaLetra = ordemEntrada[len(ordemEntrada)-1]
	codLetra    = ord(ultimaLetra)
	if codLetra == 82: # para nao repetir o S
		codLetra += 1

	if len(ordemEntrada) == 1:
		codLetra = 64

	novaLetra   = chr(codLetra+1)
	
	# atualiza vetor de estados
	ordemEntrada.append(novaLetra)
	# atualiza vetor de terminais
	conjuntoRefTerm.add(terminal)

	return novaLetra

##### Gramaticas #####
def cria_automatoGram(lista): #recebe uma string com estados e produções
	
	if len(lista) > 0:

		# print("cria automato gramatica")
		# print(lista)
		#gramatica = lista
		global dicionario, ordemEntrada

		listaEstados = str(lista).split("\n")
		# print("lista dos estados")
		# print(listaEstados)

		for estado in listaEstados: # estado tem cada estado 

			if estado != '':
				aux = estado.split('::=')
				
				chaveEstado = aux[0].replace(">","").replace("<","")
				dicionario[chaveEstado] = criaDictTerminais(aux[1])

				# lista vetor com a ordem dos estados da gramaticaS
				ordemEntrada.append(chaveEstado)

		
		# print(ordemEntrada)
		
		# print("dicionário Final\n")

		# print(dicionario)

		# print("ref terminais")
		# print(conjuntoRefTerm)

def criaDictTerminais(producoes):
	global dicionario
	listaProducoes = []
	dictProd = {}
	conjuntoTerminais = set()
	listaProducoes = producoes.split('|') # a<A> | b<B> | b | & | <B>
	
	tipo = 0
	for pr in listaProducoes:
		DP = pr.split("<") # esquerda é estado e direita é produções
		# print("duaspartes 0")
		# print(duaspartes[0])
		possuiTerminal = 0
		ter = False
		
		if DP[0] in conjuntoTerminais:

			#if len(pr) == 1 # não faz nada
			if len(pr) == 4:
				dictProd[DP[0]] =  str(dictProd[DP[0]])+str(DP[1]).replace(">","")

		else:	

			if len(pr) == 4:
				ter = DP[0]
				duaspartes  =  pr.split("<")
				dictProd[duaspartes[0]] = str(duaspartes[1]).replace(">","")

			if len(pr) == 3:
				ter = "&"
				nTerm = pr.replace("<","").replace(">","")
				dictProd[""] = nTerm

			if pr == "&":
				ter = "&"
				# dictProd[""] = ""
				tipo = 1


			if len(pr) == 1 and pr != "&":
				ter = pr
				dictProd[pr] = "X"
				dicionario['X'] = [1, {'': ''}]
				ordemEntrada.append('X')




					# bla2[duaspartes[0]] = str(bla2[duaspartes[0]])+'$'
		if ter != False and ter != "&":
			conjuntoTerminais.add(ter)
		if DP[0] != '' and DP[0] != '&':
			conjuntoRefTerm.add(DP[0])
		# print(conjuntoTerminais)
		# print('conjuntoTerminais top')

	return [tipo, dictProd]

def determiniza(dicionario, ordemEntrada, conjuntoRefTerm):
	estados  =  ordemEntrada
	for state in estados:          # i = A
		for ter in conjuntoRefTerm:    # j = a percorrendo pelos estados e pelos terminais
			if str(dicionario[state][1]).find(ter) != -1:
				# print("encontrou no find")
				ind = dicionario[state][1][ter]
				# if len(ind) == 2:
				# 	determEncontrados.add(ind)

				if len(ind) > 1 and ind not in determEncontrados: # tem indeterminismo
					internoDict = {}
					for a in conjuntoRefTerm: 
						internoDict[a] = ''
					cont = 0 
					auxState = ''
					flagFinal = 0
					for k in dicionario[state][1][ter]:   #Nao terminais que geram indeterminismo
						print(dicionario[state][1][ter][cont])
						auxState = dicionario[state][1][ter][cont]
						if dicionario[auxState][0] == 1:
							print("ACHEI UM FINAL")
							flagFinal = 1

						for t in conjuntoRefTerm:
							if str(dicionario[k][1]).find(t) != -1:

								if str(dicionario[k][1][t]) != str(internoDict[t]):
									internoDict[t] = str(dicionario[k][1][t])+str(internoDict[t])

						# ordemEntrada.remove(k)

						cont += 1
 


					dicionario[dicionario[state][1][ter]] = [flagFinal,internoDict]
					ordemEntrada.append(dicionario[state][1][ter])
					print("achou")
					print(dicionario[state][1][ter])

				if len(ind) > 1:
					determEncontrados.add(ind)

	print("determ encontrados")
	print(determEncontrados)

def minimiza(dicionario, ordemEntrada):
	for estado in ordemEntrada:
		if dicionario[estado][0] != 1:
			result = minimizacao(dicionario, estado, 0)
			print("RESULT")
			print(result)
			if result != 1:
				print("****************************************estado "+estado+" é morto")
				ordemEntrada.remove(estado)

	print("terminnou minimização")

def minimizacao(dicionario, estado, contador):
	global conjuntoRefTerm
	global ordemEntrada
	contador += 1
	

	for ter in conjuntoRefTerm:
		
		# print("isto é estado")
		# print(estado)
		# print(ter)
		if str(dicionario[estado][1]).find(ter) != -1:
			# print("procura ter")
			
			st = dicionario[estado][1][ter] # estado acessado
			if contador  >= 20:
				return 0
			if st != '' and dicionario[st][0] != 1 and st != estado:
				# print("minimização sendo chamado..st: "+st)
				# print("contador: ")
				# print(contador)
				minimizacao(dicionario, st, contador)
			elif dicionario[st][0] == 1:
				print("relaciona como encontrado um estado final na busca")
				
				return 1

def imprimeAutomato(dicionario, ordemEntrada):

	print("\n\nDicionário Final\n")
	for i in ordemEntrada:
		if dicionario[i][0] == 1:
			final = '*'
		else:
			final = ' '

		aux = final+str(i)+' => '+str(dicionario[i][1])
		print(aux)
	
	print("\n\nRef terminais")
	print(conjuntoRefTerm)
	print("\n\nOrdem Entrada")
	print(ordemEntrada)


################################# MAIN #################################
entrada = read_entrada("entrada.txt")

cria_automatoGram(separaGramaticaDeTokens(0, entrada))
cria_automatoTok(separaGramaticaDeTokens(1, entrada))
determiniza(dicionario, ordemEntrada, conjuntoRefTerm)


# print("\n\n\n\n\nref terminais")
# print(conjuntoRefTerm)
# print("Ordem Entrada")
# print(ordemEntrada)
print("dicionário Final\n")
print(dicionario)
# print("\n\n")

imprimeAutomato(dicionario, ordemEntrada)

minimiza(dicionario, ordemEntrada)

imprimeAutomato(dicionario, ordemEntrada)
