from functions import *


# MAIN
leArquivo('entrada.txt')
decodificaEntrada()
criaAutomatoGramatica()
criaProducoesToken()
determiniza()
minimiza()

print("Automato NÃO determinizado")
imprimeAutomato(dicionario, estadosEntrada)

print("Impressão determinizada")
imprimeAutomato(dicionarioDet, estadosVisitadosOrd) 

print("DICIONARIO DET")
print(dicionarioDet)

print("\n")
print("MAIN: Dicionario")
print(dicionario)
print("\n")
print("MAIN: estadosEntrada")
print(estadosEntrada)
print("\n")
print("MAIN: conjRefTerm")
print(conjuntoRefTerm)
print("estados visitados")
print(estadosVisitados)