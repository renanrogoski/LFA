# Globais
dicionario    = {} #  
dicionarioDet = {} # dicionario determinizado
dicionarioAux = {}	
entrada = ''
estadosEntrada = []  # nao terminais
conjuntoRefTerm = [] # terminais
gramaticas = ''
tokens     = ''
estadosVisitados = set()
estadosVisitadosOrd = [] # estados determinizados ordem
# Mortos
conjMortos = set()
# Para enconctrar inalcançáveis
conjAlcancaveis = set()
conjVisitadosInalc = set()
conteudoArquivo = '' # conteudo que enviara para o arquivo

def leArquivo(arquivo):
	global entrada
	f = open('arquivos/'+arquivo, 'rb')
	f.seek(0)
	entrada = f.read().decode().replace(' ', '')

def decodificaEntrada():
	global entrada
	global estadosEntrada
	global gramaticas
	global tokens	
	linhas = entrada.split('\n')
	for linha in linhas:
		if linha.find('<') != -1: # Gramática
			aux     = linha.split('::=')
			esq     = aux[0]
			entrada = esq[1:len(esq)-1] # remove <>			
			# letra repetida, gera proxima
			# if str(estadosEntrada).find(entrada) != -1 and entrada != estadosEntrada[0]: 
			# 	entradaAntiga = entrada
			# 	entrada = proximaLetra(entrada)
			# 	# Quebra linha para add possivel estado renomeado (para caso de 2 gramaticas)
			# 	linha = '<'+entrada+'>::='+aux[1]				
			# 	linha = substituiEstados(linha, entradaAntiga, entrada)
			gramaticas = str(gramaticas)+str(linha)+'\n' 
			# Insere num vetor global
			insereListaSemRep(estadosEntrada, entrada)
		else:					  # Tokens
			tokens = str(tokens)+str(linha)+'\n'

# def substituiEstados(linha, entradaAntiga, entradaNova):
# 	# Atualizar estado das producoes tbm
# 	if str(linha).find('<'+entradaAntiga+'>') != -1:
# 		linha = linha.replace(entradaAntiga, entradaNova)
# 		return linha

def proximaLetra(letra):
	global estadosEntrada
	# Caso a ultima letra seja igual a primeira
	if estadosEntrada[0] == estadosEntrada[len(estadosEntrada)-1]:
		ultimaLetra = estadosEntrada[len(estadosEntrada)-2]
	else:
		ultimaLetra = estadosEntrada[len(estadosEntrada)-1]
	cod = ord(ultimaLetra)
	if cod == 82: # para nao repetir o S
		cod += 1
	proxLetra = chr(cod+1)
	return proxLetra

def criaAutomatoGramatica():
	global dicionario
	global gramaticas
	estadosTemp = []

	linhas = gramaticas.split('\n')
	indice = 0
	for linha in linhas:
		if linha != '':
			partes = linha.split('::=')
			estado = partes[0][1:len(partes[0])-1]
			if estado in estadosTemp: # estado repetido, concatena
				linhas[0] = str(linhas[0])+'|'+partes[1]
				#linhas[indice] = ''
				linhas.remove(linhas[indice])
			

			# print('prod')
			# print(partes[1])

			estadosTemp.append(estado)
			indice += 1


	for linha in linhas:
		print('LINHAAA')
		print(linha)
		if linha != '':
			partes = linha.split('::=')
			estado = partes[0][1:len(partes[0])-1]
			dicionario[estado] = criaProducoesGramatica(partes[1])
			

	print("Tripão Gramaticas")
	print(dicionario)
	# print('gramaticas')
	# print(gramaticas)

def criaProducoesGramatica(producoes):
	dicionarioInterno = {}
	flagFinal = 0
	conjuntoRefTermTmp = set()
	producoes = producoes.split('|')
	for producao in producoes:
		if len(producao) == 1: # terminal sozinho -> estado de erro
			if producao != 'ε':
				#conjuntoRefTerm.add(producao)
				insereListaSemRep(conjuntoRefTerm, producao)
				if producao not in conjuntoRefTermTmp:
					dicionarioInterno[producao] = 'Z' # estado de erro
				else:
					dicionarioInterno[producao] = str(dicionarioInterno[producao])+'Z' # estado de erro
				conjuntoRefTermTmp.add(producao)
				dicionario['Z'] = [1, {'':''}]
				insereListaSemRep(estadosEntrada, 'Z')
			else: 								# ε
				flagFinal = 1 # estado sera final
		else: # terminal nao esta sozinho
			aux      = producao.split('<')
			terminal = aux[0]
			estado   = aux[1].replace('>', '')
			conjuntoRefTermTmp.add(terminal)
			#conjuntoRefTerm.add(terminal)
			insereListaSemRep(conjuntoRefTerm, terminal)
			if str(dicionarioInterno).find(terminal) != -1: # encontrou
				dicionarioInterno[terminal] = str(dicionarioInterno[terminal])+str(estado)
			else:
				dicionarioInterno[terminal] = estado

	return [flagFinal, dicionarioInterno]

def criaProducoesToken():
	global estadosEntrada
	global tokens
	global dicionario
	
	linha = tokens.split("\n")	
	for i in linha:
		if i != '':	    # cada token
			cont = 0
			for j in i: # cada caractere do token
				if cont == 0: # primeiro caracterer do token
					if dicionario == {}:
						dicionario['S'] = [0, {j:''}]
						estadosEntrada.append('S')
					if j in dicionario['S'][1]: # encontrou o caractere do token
						estadoFinal = buscaProxEstado(j)
						dicionario['S'][1][j] = str(dicionario['S'][1][j])+str(estadoFinal)
					else:
						estadoFinal = buscaProxEstado(j)
						dicionario['S'][1][j] = estadoFinal
				else: # gera um novo estado...
					proximoEstado = estadosEntrada[len(estadosEntrada)-1]
					estadoFinal = buscaProxEstado(j)
					dicionario[proximoEstado] = [0, {j:estadoFinal}]
					dicionario[proximoEstado][1][j] = estadosEntrada[len(estadosEntrada)-1]
				
				# Valida se eh estado final ou nao
				if cont == len(i)-1: # ultima letra do token... gera um estado final
					dicionario[estadoFinal] = [1, {'':''}]

				cont += 1

def buscaProxEstado(terminal):
	global estadosEntrada, conjuntoRefTerm
	if estadosEntrada[len(estadosEntrada)-1] == 'Z':
		ultimaLetra = estadosEntrada[len(estadosEntrada)-2]
	else:
		ultimaLetra = estadosEntrada[len(estadosEntrada)-1]
	codLetra    = ord(ultimaLetra)
	if codLetra == 82: # para nao repetir o S
		codLetra += 1
	if len(estadosEntrada) == 1: # para criar A
		codLetra = 64
	novaLetra = chr(codLetra+1)	
	# atualiza vetor de estados
	estadosEntrada.append(novaLetra)
	# atualiza vetor de terminais
	#conjuntoRefTerm.add(terminal)
	insereListaSemRep(conjuntoRefTerm, terminal)
	return novaLetra

def insereListaSemRep(lista, vlr):
	if str(lista).find(vlr) == -1: # ainda nao existe na lista, pode add
		lista.append(vlr)

def determiniza():
	global dicionario
	global dicionarioDet
	global estadosEntrada
	global conjuntoRefTerm
	global dicionarioAux
	global estadosVisitados
	global estadosVisitadosOrd
	
	dicionarioAux = dicionario

	ordemDeterm = []
	ordemDetermX = set()
	insereListaSemRep(ordemDeterm, estadosEntrada[0])

	dicionarioDet[estadosEntrada[0]] = dicionario[estadosEntrada[0]] # dicionario de S
	print("Dicinário determinizado")
	print(dicionarioDet)

	print("OrdemDeterm")
	print(ordemDeterm)
	# rp = 0
	while 1:
		# rp < 12
		# rp += 1
		if ordemDeterm == '' or ordemDeterm == []:
			return
		
		# insereListaSemRep(estadosVisitados, ordemDeterm[0])
		
		if ordemDeterm[0] not in estadosVisitados:
			estadosVisitadosOrd.append(ordemDeterm[0])
		estadosVisitados.add(ordemDeterm[0])		

		print("Estados visitados")
		print(estadosVisitados)
		print(estadosVisitadosOrd)

		for terminal in conjuntoRefTerm:			
			if str(dicionarioAux[ordemDeterm[0]][1]).find(terminal) != -1: # este terminal existe neste estado
				# insereListaSemRep(ordemDeterm, dicionarioAux[ordemDeterm[0]][1][terminal])
				if dicionarioAux[ordemDeterm[0]][1][terminal] not in ordemDetermX and dicionarioAux[ordemDeterm[0]][1][terminal] != '':
					ordemDeterm.append(dicionarioAux[ordemDeterm[0]][1][terminal])
				ordemDetermX.add(dicionarioAux[ordemDeterm[0]][1][terminal])	
	
		# passa o primeiro valor da lista de ordem (S) para determinizar a linha no dicionarioDet
		ordemDeterm.pop(0)

		if len(ordemDeterm) > 0 and ordemDeterm[0] not in estadosVisitados:

			if len(ordemDeterm) > 0 and len(ordemDeterm[0]) > 1: #lista não esta vazia e há indeterminismo
		
				determinizaLinha(ordemDeterm[0])
			if ordemDeterm[0] != '':
				dicionarioDet[ordemDeterm[0]] = dicionarioAux[ordemDeterm[0]]
			# insereListaSemRep(estadosVisitados, ordemDeterm[0])
		print("ordemDeterm")
		print(ordemDeterm)
		print("\n")

	print('PILHA')
	print(ordemDeterm)
	print("Dicinário determinizado")
	print(dicionarioDet)

def determinizaLinha(estado):
	global conjuntoRefTerm
	global dicionarioAux
	flagFinal = 0
	dicionarioInterno = {}
	# concatena
	for a in conjuntoRefTerm: 
		dicionarioInterno[a] = ''

	for letra in estado:
		for terminal in conjuntoRefTerm: 
			# Verifica se concatenacao nao repete nenhuma letra
			if str(dicionarioAux[letra][1]).find(terminal) != -1:
				print("ero")
				print(str(dicionarioInterno[terminal])+"*******"+str(dicionarioAux[letra][1][terminal]))
				#  valida para não concatenar as mesmas letras
				if str(dicionarioInterno[terminal]).find(dicionarioAux[letra][1][terminal]) == -1: # não encontrou 

					dicionarioInterno[terminal] = str(dicionarioInterno[terminal])+str(dicionarioAux[letra][1][terminal])
					print(dicionarioInterno[terminal])

		# Verifica se este estado eh final
		if dicionarioAux[letra][0] == 1:
			flagFinal = 1

	dicionarioAux[estado] = [flagFinal, dicionarioInterno]

def minimiza(): 
	global estadosVisitadosOrd
	# Mortos
	for estado in estadosVisitadosOrd:	
		minimizaMortos(estado)
	# Inalcançáveis
	#minimizaInalcancaveis(estadosVisitadosOrd[0]) # Envia apenas o primeiro estado

####### MORTOS ######
def minimizaMortos(estado):
	global conjuntoRefTerm
	global dicionarioDet

	for terminal in conjuntoRefTerm:
		if str(dicionarioDet[estado][1]).find(terminal) != -1: # existe esse terminal em S
			aux = ''
			for producoes in dicionarioDet[estado][1][terminal]: # varre todas as producoes do estado S
				aux = str(aux)+str(producoes)
			producao = aux
			
			minimizaMortosProducoes(producao, 0) # funcao que busca ebsolon somente nas producoes deste estado

def minimizaMortosProducoes(estado, qtd):
	global conjuntoRefTerm
	global conjMortos
	global dicionarioDet
	qtd += 1
	for terminal in conjuntoRefTerm:
		if estado != '' and dicionarioDet[estado][0] == 0: # nao eh final			
			if str(dicionarioDet[estado][1]).find(terminal) != -1:
				if qtd < 20:
					minimizaMortosProducoes(dicionarioDet[estado][1][terminal], qtd)
				else: 
					# MORTO
					if dicionarioDet[estado][0] == 0: # nao eh final
						conjMortos.add(estado) # primeiro estado do loop
					if dicionarioDet[dicionarioDet[estado][1][terminal]][0] == 0: # nao eh final
						conjMortos.add(dicionarioDet[estado][1][terminal]) # segundo estado do loop

def imprimeAutomato(tipo, exibeMorto, dicionario, estadosEntrada, mensagem):
	global conjuntoRefTerm
	global conteudoArquivo

	dicionarioPrint = dicionario

	# Limpar 
	for i in estadosEntrada:
		for j in conjuntoRefTerm:
			if str(dicionarioPrint[i][1]).find(j) == -1: # Não encontrou
				dicionarioPrint[i][1][j] = ' -- '

	matriz = str(mensagem)+'\n\n'
	matriz = str(matriz)+' |  δ\t'
	for i in conjuntoRefTerm: # exibe todas as letrinhas
		matriz = str(matriz)+' | '+i+'\t'
	matriz = str(matriz)+' |\n'
	matriz = str(matriz)+' ---------'
	for i in conjuntoRefTerm: # exibe todas as letrinhas
		matriz = str(matriz)+'--------'
	matriz = str(matriz)+'\n'
		
	for i in estadosEntrada:
		if exibeMorto == 1 or (exibeMorto == 0 and i not in conjMortos and tipo == 1):
			#
			if dicionarioPrint[i][0] == 1:
				final = '*'
			else:
				final = ' '
			matriz = str(matriz)+' | '+final+i+'\t'

			for j in conjuntoRefTerm:
				matriz = str(matriz)+' | '+dicionarioPrint[i][1][j]+"\t"
			
			# Verifica se é morto
			morto = ' | '
			if i in conjMortos and tipo == 1: # é morto
				morto = ' | Morto'

			matriz = str(matriz)+morto+'\n'

	print(matriz)
	# Concatena na variavel global para enviar tudo para arquivo de saída
	conteudoArquivo = str(conteudoArquivo)+str(matriz)	

def escreveArquivo():
	global conteudoArquivo
	arquivo = open('arquivos/saida.txt', 'w')
	arquivo.truncate() # limpa arquivo, para caso de salvar arquivo ja existente
	arquivo.seek(0)
	arquivo.write(conteudoArquivo)
	arquivo.close()

def minimizaInalcancaveis(estado): # recebe apenas o estado inicial
	global conjAlcancaveis
	global conjuntoRefTerm
	global dicionario
	global conjVisitadosInalc
	
	conjVisitadosInalc.add(estado)

	conjAlcancaveis.add(estado) # insere o primeiro estado

	for terminal in conjuntoRefTerm:
		if str(dicionario[estado][1]).find(terminal) != -1: # existe esse terminal em S
			aux = ''
			
			for producoes in dicionario[estado][1][terminal]: 
				aux = str(aux)+str(producoes)
			producao = aux
			# estado ainda nao criado, anal. separadamente
			if len(producao) > 1: 
				for cadaCaractEst in producao:
					# funcao que busca ebsolon somente nas producoes deste estado
					minimizaInalcancaveisProducoes(cadaCaractEst, 0)
					conjAlcancaveis.add(cadaCaractEst) 
			else:
				minimizaInalcancaveisProducoes(producao, 0)
				conjAlcancaveis.add(producao)			

def minimizaInalcancaveisProducoes(estado, qtd):
	global conjuntoRefTerm
	global conjAlcancaveis
	global dicionarioDet
	global conjVisitadosInalc
	qtd += 1
	for terminal in conjuntoRefTerm:
		if estado != '' and str(dicionarioDet[estado][1]).find(terminal) != -1:
			
			conjVisitadosInalc.add(dicionarioDet[estado][1][terminal])
			
			if proximoEstado in conjVisitadosInalc and qtd < 20: # Ok
				print('estado')
				print(estado)
				proximoEstado = dicionarioDet[estado][1][terminal]
				# Encontrou um alcançado
				conjAlcancaveis.add(proximoEstado)
				#				
				minimizaInalcancaveisProducoes(proximoEstado, qtd)
			else: # deu loop
				print('Deu loop')
				return 