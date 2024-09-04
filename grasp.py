import tsplib95
import math
import random

def lerCoordenadas(arquivo):
    problema = tsplib95.load(arquivo)
    coordenadas_pontos = {node: coord for node, coord in problema.node_coords.items()}
    return coordenadas_pontos

def construcaoGulosaRandomica(LRC):
    LC = set(LRC)
    solucao = []
    while LC:
        lrc = list(LC)
        selecionado = random.choice(lrc)
        solucao.append(selecionado)
        LC.remove(selecionado)
    return solucao

def calcularDistancia(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calcularQualidade(solucao, coordenadas_pontos):
    distancia_total = 0
    for i in range(len(solucao) - 1):
        ponto_atual = coordenadas_pontos[solucao[i]]
        proximo_ponto = coordenadas_pontos[solucao[i + 1]]
        distancia = calcularDistancia(ponto_atual, proximo_ponto)
        distancia_total += distancia
    ponto_inicio = coordenadas_pontos[solucao[0]]
    ponto_fim = coordenadas_pontos[solucao[-1]]
    distancia_retorno = calcularDistancia(ponto_fim, ponto_inicio)
    distancia_total += distancia_retorno
    return -distancia_total  

def Vizinhaca(solucao):
    vizinhaca = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            vizinha = solucao[:]
            vizinha[i], vizinha[j] = vizinha[j], vizinha[i]
            vizinhaca.append(vizinha)
    return vizinhaca

def buscaLocal(solucao, coordenadas_pontos):
    solucao_atual = solucao
    while True:
        melhor_solucao = None
        melhor_qualidade = calcularQualidade(solucao_atual, coordenadas_pontos)
        vizinhaca = Vizinhaca(solucao_atual)
        for vizinha in vizinhaca:
            qualidade_vizinha = calcularQualidade(vizinha, coordenadas_pontos)
            if qualidade_vizinha > melhor_qualidade:
                melhor_solucao = vizinha
                melhor_qualidade = qualidade_vizinha
        if melhor_solucao is None:
            break
        solucao_atual = melhor_solucao
    return solucao_atual

def atualizarSolucao(solucao, melhorSolucao, coordenadas_pontos):
    if melhorSolucao is None:
        return solucao
    return solucao if calcularQualidade(solucao, coordenadas_pontos) > calcularQualidade(melhorSolucao, coordenadas_pontos) else melhorSolucao

def GRASP(maxInteracoes, LRC, coordenadas_pontos):
    melhorSolucao = None
    for _ in range(maxInteracoes):
        solucao = construcaoGulosaRandomica(LRC)
        solucao = buscaLocal(solucao, coordenadas_pontos)
        melhorSolucao = atualizarSolucao(solucao, melhorSolucao, coordenadas_pontos)
    return melhorSolucao

def main():
    arquivo = 'Caixeiro-Viajante/berlin52.tsp'
    coordenadas_pontos = lerCoordenadas(arquivo)
    LRC = list(coordenadas_pontos.keys())
    maxInteracoes = 100  
    melhorSolucao = GRASP(maxInteracoes, LRC, coordenadas_pontos)
    if melhorSolucao:
        distancia_total = -calcularQualidade(melhorSolucao, coordenadas_pontos)
        print(f"\nMelhor Solucao:\n {melhorSolucao} \nDistância Total: {distancia_total}")
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
