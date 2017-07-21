# Globais
dicionario = {}
entrada = ''
estadosEntrada = []		# nao terminais
conjuntoRefTerm = set() # terminais
gramaticas = ''
tokens     = ''

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

	linhas = gramaticas.split('\n')

	for linha in linhas:
		if linha != '':
			partes = linha.split('::=')
			estado = partes[0][1:len(partes[0])-1]
			dicionario[estado] = criaProducoesGramatica(partes[1])


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
				conjuntoRefTerm.add(producao)
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
			conjuntoRefTerm.add(terminal)
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
					# print("gamb")
					# print(dicionario)
					if dicionario == {}:
						# print('Dicionario novo')
						dicionario['S'] = [0, {j:''}]
						estadosEntrada.append('S')
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
					proximoEstado = estadosEntrada[len(estadosEntrada)-1]
					# print("novo estado")
					# print(proximoEstado)
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
	conjuntoRefTerm.add(terminal)
	return novaLetra

def imprimeAutomato(dicionario, estadosEntrada):
	print("\n\nDicionario Final\n")
	for i in estadosEntrada:
		if dicionario[i][0] == 1:
			final = '*'
		else:
			final = ' '

		aux = final+str(i)+' => '+str(dicionario[i][1])
		print(aux)
	
	# print("\n\nRef terminais")
	# print(conjuntoRefTerm)
	# print("\n\nOrdem Entrada")
	# print(ordemEntrada)

def insereListaSemRep(lista, vlr):
	if str(lista).find(vlr) == -1: # ainda nao existe na lista, pode add
		lista.append(vlr)
