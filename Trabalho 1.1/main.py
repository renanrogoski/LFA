from functions import *

leArquivo('entrada.txt')
decodificaEntrada()
criaAutomatoGramatica()
criaProducoesToken()
determiniza()
minimiza() 
imprimeAutomato(0, 1, dicionario, estadosEntrada, "\n\n*** AUTÔMATO ***\n")
imprimeAutomato(1, 1, dicionarioDet, estadosVisitadosOrd, "\n\n*** AUTÔMATO DETERMINIZADO ***\n") 
imprimeAutomato(1, 0, dicionarioDet, estadosVisitadosOrd, "\n\n*** AUTÔMATO DETERMINIZADO E MINIMIZADO***\n") 
escreveArquivo() 