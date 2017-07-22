from functions import *


# MAIN
leArquivo('entrada.txt')
decodificaEntrada()
criaAutomatoGramatica()
criaProducoesToken()
determiniza()
minimiza() 
imprimeAutomato(0, dicionario, estadosEntrada, "\n\n*** AUTÔMATO ***\n")
imprimeAutomato(1, dicionarioDet, estadosVisitadosOrd, "\n\n*** AUTÔMATO DETERMINIZADO ***\n") 