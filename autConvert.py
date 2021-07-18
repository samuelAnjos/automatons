# encoding: utf-8

from Estado import Estado
from Transicao import Transicao
import xml.etree.ElementTree as ET #ler xml
from itertools import combinations #combinar estados
import random #gerar eixoX e eixoY
import sys #passar arquivos como argumento


#coding

#arquivo = "q_teste.jff"
#arquivo = "q_Slide.jff"
#arquivo = "aut_TesteT.jff"
#arquivo = "autcomlambda.jff"
#arquivo = "aut_SLIDE_DET.jff"



print("------Automaton Converter-------")

try:
    arquivo = str(sys.argv[1])
    arquivo_salvar = str(sys.argv[2])
except:
    #print("Quick use: python main.py nome_automato_ND nome_automato_DT")
    print("Uso Rápido: python autConvert.py nome_autômato_ND nome_automato_DT")
    arquivo = str(input("Digite o nome do autômato NÃO Deterministico: "))
    arquivo_salvar = str(input("Digite o nome do autômato Deterministico a ser salvo: "))

if arquivo.__contains__(".jff") == False:
    arquivo += '.jff'

if arquivo_salvar.__contains__(".jff") == False:
    arquivo_salvar += '.jff'


tree = ET.parse(arquivo)
root = tree.getroot()


simbolos_xml = []

for child in root.iter("read"):
    if simbolos_xml.__contains__(child.text) == False and child.text != None:
        simbolos_xml.append(child.text)

for child in root.iter("read"):
    if simbolos_xml.__contains__("E") == False and child.text == None:
        simbolos_xml.append("E")


def pegarEstados(arquivo):
    tree = ET.parse(arquivo)
    root = tree.getroot()

    listEstados = []

    filtro = "*"

    for child in root.iter(filtro):
        estados = child.findall("state")
        for estado in estados:
            eFinal = False
            eInicial = False

            id = estado.attrib.get("id")
            nome = estado.attrib.get("name")

            for fim in estado:
                if fim.tag == "final":
                    eFinal = True
            for inicio in estado:
                if inicio.tag == "initial":
                    eInicial = True

            listEstados.append(Estado("100", "100", eFinal, eInicial, id, nome))

    return listEstados


def compararArquivoComLista(de_arquivo,
                            lista):  # essa função serve para compara o que está sendo lido nas transicoes do XML com o id atribuido ao objeto Estado
    for item in list(lista):
        if (de_arquivo == item.__getattribute__("_id")):
            return item  # retorna o Estado com o id igual ao lido pelo xml



def pegarTransicoes(arquivo, listEstados):
    tree = ET.parse(arquivo)
    root = tree.getroot()

    listTransicoes = []  # lista usada para armazenas todas as transições em forma de objeto
    listOrigem = []
    listDestino = []
    listLido = []

    filtro = "*"

    for child in root.iter(filtro):
        transicoes = child.findall("transition")  # filtra em busca de transicoes
        for transicao in transicoes:
            de = '-1'
            para = '-1'
            lido = '-1'
            for origem in transicao:  # em cada transicao ele tem um origem diferente. origem pode ser "from", "to" ou "read"
                if origem.tag == "from":
                    de = origem.text
                    listOrigem.append(compararArquivoComLista(de,
                                                              listEstados))  # adiciona o estado que possui o seu atributo _id == ao valor lido no xml
                elif origem.tag == "to":
                    para = origem.text ###
                    listDestino.append(compararArquivoComLista(para, listEstados))
                elif origem.tag == "read":
                    lido = origem.text
                    if lido == None:
                        listLido.append("E")
                    else:
                        listLido.append(lido)



    for i in range(len(listOrigem)):
        listTransicoes.append(Transicao(listOrigem[i], listDestino[i], listLido[
            i]))  # cria uma lista com todas as transições, onde cada tansição recebe um objeto estado como origem e como destino e o inteiro que é o valor lido no xml

    return listTransicoes  # retorna a lista de transicoes com vários objetos da classe Transicao.



def verificaAutomato(arquivo2):
    tree = ET.parse(arquivo)
    root = tree.getroot()

    NaoDeterministico = False

    if simbolos_xml.__contains__("E"): #Se o arquivo tiver o Lambda, ele já passa a ser Não Determinístico
        return True

    combinacao_from_read = []

    for auto in root.findall("automaton"):
        for transicao in auto.findall("transition"):
            for saida in transicao.findall("from"):
                saida = saida
            for lido in transicao.findall("read"):
                lido = lido
            combinacao_from_read.append(saida.text + lido.text)

    for combincao in combinacao_from_read:
        if combinacao_from_read.count(combincao) > 1: #compara se existem duas strings iguais na lista [saido+lido]
            NaoDeterministico = True

    return NaoDeterministico



def compararEstadoComTransicao(tamanho, elementoLista, Transicoes, EstadosDEFOBJ):
    if simbolos_xml.__contains__("E"):
        return compararEstadoComTransicao3E(elementoLista, Transicoes, EstadosDEFOBJ) #para automato com Lambda
    if tamanho == 2:
        return compararEstadoComTransicao2(elementoLista, Transicoes) #para automato com 2 simbolos
    elif tamanho == 3:
        return compararEstadoComTransicao3(elementoLista, Transicoes) #para automato com 3 simbolos



def compararEstadoComTransicao2(elementoLista, Transicoes):
    lista = []
    listapara0 = []
    listapara1 = []

    if type(elementoLista) == type(lista):
        for elemento in elementoLista:
            for transicao in Transicoes:
                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[0]:
                    if listapara0.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara0.append(transicao.estadoFinal.__getattribute__("_nome"))

                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[1]:
                    if listapara1.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara1.append(transicao.estadoFinal.__getattribute__("_nome"))
    else:
        for transicao in Transicoes:
            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[0]:
                listapara0.append(transicao.estadoFinal.__getattribute__("_nome"))
            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[1]:
                listapara1.append(transicao.estadoFinal.__getattribute__("_nome"))

    listaTransicoes = [listapara0, listapara1]

    return listaTransicoes



def compararEstadoComTransicao3(elementoLista, Transicoes):
    lista = []
    listapara0 = []
    listapara1 = []
    listapara2 = []

    if type(elementoLista) == type(lista):
        for elemento in elementoLista:
            for transicao in Transicoes:
                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[0]:
                    if listapara0.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara0.append(transicao.estadoFinal.__getattribute__("_nome"))

                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[1]:
                    if listapara1.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara1.append(transicao.estadoFinal.__getattribute__("_nome"))

                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[2]:
                    if listapara2.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara2.append(transicao.estadoFinal.__getattribute__("_nome"))

    else:
        for transicao in Transicoes:
            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[0]:
                listapara0.append(transicao.estadoFinal.__getattribute__("_nome"))
            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[1]:
                listapara1.append(transicao.estadoFinal.__getattribute__("_nome"))
            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[2]:
                listapara2.append(transicao.estadoFinal.__getattribute__("_nome"))

    listaTransicoes = [listapara0, listapara1, listapara2]

    return listaTransicoes


def pegarEstadoInicial(EstadosDEFOBJ):
    for estado in EstadosDEFOBJ:
        if estado.__getattribute__("_isInitial") == True:
            return estado.__getattribute__("_nome")



def compararEstadoComTransicao3E(elementoLista, Transicoes, EstadosDEFOBJ):
    lista = []
    listapara0 = []
    listapara1 = []
    listaparaE = []
    ligacaoE = []

    estadoInicial = pegarEstadoInicial(EstadosDEFOBJ)


    if type(elementoLista) == type(lista):
        for elemento in elementoLista:
            for transicao in Transicoes:
                if elemento == transicao.estadoFinal.__getattribute__(
                        "_nome") and transicao.simbolo == "E":
                    for tran in Transicoes:
                        if (transicao.estadoInicial.__getattribute__("_nome") == tran.estadoFinal.__getattribute__(
                                "_nome")) and elemento != estadoInicial:

                            ligacaoE = transicao.estadoInicial.__getattribute__(
                                "_nome") + ';' + tran.estadoInicial.__getattribute__("_nome")

                            if tran.simbolo == simbolos_xml[0]:
                                listapara0.append((ligacaoE.split(';')))
                            else:
                                listapara1.append((ligacaoE.split(';')))


                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[0]:
                    if listapara0.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara0.append(transicao.estadoFinal.__getattribute__("_nome"))

                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[1]:
                    if listapara1.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listapara1.append(transicao.estadoFinal.__getattribute__("_nome"))

                if elemento == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[2]:
                    if listaparaE.count(transicao.estadoFinal.__getattribute__("_nome")) == 0:
                        listaparaE.append(transicao.estadoFinal.__getattribute__("_nome"))

    else:
        for transicao in Transicoes:
            if elementoLista == transicao.estadoFinal.__getattribute__("_nome") and transicao.simbolo == "E": #talvez esteja errado
               for tran in Transicoes:
                    if (transicao.estadoInicial.__getattribute__("_nome") == tran.estadoFinal.__getattribute__("_nome")) and elementoLista != estadoInicial:

                        ligacaoE = transicao.estadoInicial.__getattribute__("_nome") + ';' + tran.estadoInicial.__getattribute__("_nome")

                        if tran.simbolo == simbolos_xml[0]:
                            listapara0.append((ligacaoE.split(';')))
                        else:
                            listapara1.append((ligacaoE.split(';')))

            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[0]:
                listapara0.append(transicao.estadoFinal.__getattribute__("_nome"))
            if elementoLista == transicao.estadoInicial.__getattribute__("_nome") and transicao.simbolo == simbolos_xml[1]:
                listapara1.append(transicao.estadoFinal.__getattribute__("_nome"))


    novalistaA = []
    novalistaB = []

    for i in range(len(listapara0)):
        for c in listapara0[i]:
            novalistaA.append(c)

    for item in novalistaA:
        if novalistaA.count(item)>1:
            novalistaA.remove(item)



    for i in range(len(listapara1)):
        for c in listapara1[i]:
            novalistaB.append(c)

    for item in novalistaB:
        if novalistaB.count(item)>1:
            novalistaB.remove(item)

    listaTransicoes = [novalistaA, novalistaB, listaparaE]

    return listaTransicoes



def criarTransicao(estadoSaida, estadoEntrada, j):
    lista = []

    if (type(estadoEntrada) == type(lista)) and len(estadoEntrada) == 1:
        return Transicao(estadoSaida, estadoEntrada[0], simbolos_xml[j])

    return Transicao(estadoSaida, estadoEntrada, simbolos_xml[j])


def criarEstados(listaEstadosDEF, Estados):
    EstadosOBJ = []
    EstadosFinais = []
    estadoInicial = ""
    id = 0


    for estado in Estados:
        if estado.__getattribute__("_isFinal") == True:
            EstadosFinais.append(estado.__getattribute__("_nome"))

    for estado in Estados:
        if estado.__getattribute__("_isInitial") == True:
            estadoInicial = estado.__getattribute__("_nome")

    for estado in listaEstadosDEF:
        eFinal = False
        eInicial = False
        for estadofim in EstadosFinais:
            if estado.__contains__(estadofim):
                eFinal = True
        if estado == estadoInicial:
            eInicial = True
        EstadosOBJ.append(Estado(random.randint(10, 900), random.randint(10, 900), eFinal, eInicial, id, estado))
        id += 1

    return EstadosOBJ



def trocarEstadoInicial(EstadosDEFOBJ, TransicoesDET):
    estado_inicial = []
    listaAUX = []

    for estado in EstadosDEFOBJ:
        if estado.__getattribute__("_isInitial"):
            estado_inicial = estado.__getattribute__("_nome")
            estado.__setattr__("_isInitial", False)


    for child in root.iter("read"):
        if child.text == None:
            child.text = "E"
        listaAUX.append(child.text)


    for transicao in TransicoesDET:
        if transicao.estadoInicial.__contains__(estado_inicial) and transicao.simbolo == "E":
            if transicao.estadoInicial.__contains__(transicao.estadoFinal) and listaAUX.count("E")+1 == len(transicao.estadoInicial):
                estado_inicial = transicao.estadoInicial


    for estado in EstadosDEFOBJ:
        if estado.__getattribute__("_nome").split(';') == estado_inicial:
            estado.__setattr__("_isInitial", True)
        elif estado.__getattribute__("_nome") == estado_inicial:
            estado.__setattr__("_isInitial", True)






def pegarID(EstadosDEFOBJ, transicao, status):

    for estado in EstadosDEFOBJ:
        if estado.__getattribute__("_nome").__contains__(";"):
           if transicao.__getattribute__(status) == estado.__getattribute__("_nome").split(";"):
                return estado.__getattribute__("_id")
        else:
            if transicao.__getattribute__(status) == estado.__getattribute__("_nome"):
                return estado.__getattribute__("_id")


def criarArquivoDET(EstadosDEFOBJ, TransicoesDET):
    estados = []

    #arquivoDET = open("aut_SLIDE_DET.jff", "w")
    arquivoDET = open(arquivo_salvar, "w")
    arquivoDET.write(
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 6.4.--><structure>&#13;\n')
    arquivoDET.write('	<type>fa</type>&#13;\n')
    arquivoDET.write('	<automaton>&#13;\n')
    arquivoDET.write('		<!--The list of states.-->&#13;\n')

    for estado in EstadosDEFOBJ:
        arquivoDET.write('		<state id="{}" name="{}">&#13;\n'.format(estado.__getattribute__("_id"),estado.__getattribute__("_nome")))
        arquivoDET.write('			<x>{}.0</x>&#13;\n			<y>{}.0</y>&#13;\n'.format(estado.__getattribute__("_posX"),estado.__getattribute__("_posY")))
        if estado.__getattribute__("_isInitial"):
            arquivoDET.write('			<initial/>&#13;\n')
        if estado.__getattribute__("_isFinal"):
            arquivoDET.write('			<final/>&#13;\n')
        arquivoDET.write('		</state>&#13;\n')
        estados.append(estado)

    arquivoDET.write('		<!--The list of transitions.-->&#13;\n')


    for transicao in TransicoesDET:
        arquivoDET.write('		<transition>&#13;\n')
        arquivoDET.write('			<from>{}</from>&#13;\n'.format(pegarID(EstadosDEFOBJ, transicao, "estadoInicial")))
        arquivoDET.write('			<to>{}</to>&#13;\n'.format(pegarID(EstadosDEFOBJ, transicao, "estadoFinal")))
        if transicao.__getattribute__("simbolo") == "E":
            arquivoDET.write('			<read/>&#13;\n')
        else:
            arquivoDET.write('			<read>{}</read>&#13;\n'.format(transicao.__getattribute__("simbolo")))
        arquivoDET.write('		</transition>&#13;\n')


    arquivoDET.write('	</automaton>&#13;\n')
    arquivoDET.write('</structure>')

    arquivoDET.close()

if __name__ == "__main__":

    if(verificaAutomato(arquivo) == True): #Verifica se é não determinístico

        Estados = pegarEstados(arquivo)
        #combEstados = []

        Estados_nome = []


        for i in range(len(Estados)):
            Estados_nome.append(Estados[i].__getattribute__("_nome"))


        Transicoes = pegarTransicoes(arquivo, Estados)


        Lista = []

        for i in range(len(
                Estados) + 1):
            if i > 0:
                Lista.append([';'.join(str(c) for c in palavra) for palavra in combinations(Estados_nome, i)])


        saidasDET = []
        entradasDET = []
        lidosDET = []

        TransicoesAUX = []
        TransicoesDETE = []
        TransicoesDET = []

        listaEstadosDEF = []

        for estado in Lista:
            for elemento in estado:
                listaEstadosDEF.append(elemento)

        EstadosDEFOBJ = criarEstados(listaEstadosDEF, Estados)

        precisaTirarOLambda = False

        for i in range(len(Lista)):
            for elemento in Lista[i]:
                if elemento.count(";") == 0:
                    elemento = elemento

                if elemento.count(";") > 0:
                    elemento = elemento.split(";")
                saidasDET.append(elemento)

                TransicoesAUX = compararEstadoComTransicao(len(simbolos_xml), elemento, Transicoes, EstadosDEFOBJ)

                if simbolos_xml.__contains__("E"):
                    for j in range(len(simbolos_xml)):
                        if criarTransicao(elemento, TransicoesAUX[j], j) != None and len(TransicoesAUX[j]) > 0:
                            TransicoesDET.append(criarTransicao(elemento, sorted(TransicoesAUX[j]), j))
                    precisaTirarOLambda = True
                else:
                    for j in range(len(simbolos_xml)):
                        if criarTransicao(elemento, TransicoesAUX[j], j) != None and len(TransicoesAUX[j]) > 0:
                            TransicoesDET.append(criarTransicao(elemento, sorted(TransicoesAUX[j]), j))

        if precisaTirarOLambda:
            trocarEstadoInicial(EstadosDEFOBJ, TransicoesDET)
            for transicao in TransicoesDET:
                if transicao.__getattribute__("simbolo") == "E":
                    TransicoesDET.remove(transicao)



        criarArquivoDET(EstadosDEFOBJ, TransicoesDET)
        print("Arquivo {} criado com sucesso!".format(arquivo_salvar))

    else:
        print("Impossível converter o autômato, ele já é determinístico!")

