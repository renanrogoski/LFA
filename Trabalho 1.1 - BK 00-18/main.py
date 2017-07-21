from functions import *


# MAIN
leArquivo('entrada.txt')
decodificaEntrada()
criaAutomatoGramatica()
criaProducoesToken()
imprimeAutomato(dicionario, estadosEntrada)





print("\n")
print("MAIN: Dicionario")
print(dicionario)
print("\n")
print("MAIN: estadosEntrada")
print(estadosEntrada)
print("\n")
print("MAIN: conjRefTerm")
print(conjuntoRefTerm)