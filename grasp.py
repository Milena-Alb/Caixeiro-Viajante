import math
import random

def lerCoordenadas(arquivo):
    pontos_matriz = {}
    with open(arquivo, 'r') as rota:
        for linha in rota:
            if linha.startswith("NODE_COORD_SECTION"):
                break
        for linha in rota:
            if linha.strip() == "EOF":
                break
            dados = linha.strip().split()
            ponto = int(dados[0])
            x, y = float(dados[1]), float(dados[2])
            pontos_matriz[ponto] = (x, y)
    return pontos_matriz

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

def calcularQualidade(solucao, pontos_matriz):
    distancia_total = 0
    for i in range(len(solucao) - 1):
        ponto_atual = pontos_matriz[solucao[i]]
        proximo_ponto = pontos_matriz[solucao[i + 1]]
        distancia = calcularDistancia(ponto_atual, proximo_ponto)
        distancia_total += distancia
    ponto_inicio = pontos_matriz[solucao[0]]
    ponto_fim = pontos_matriz[solucao[-1]]
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

def buscaLocal(solucao, pontos_matriz):
    solucao_atual = solucao
    while True:
        melhor_solucao = None
        melhor_qualidade = calcularQualidade(solucao_atual, pontos_matriz)
        vizinhaca = Vizinhaca(solucao_atual)
        for vizinha in vizinhaca:
            qualidade_vizinha = calcularQualidade(vizinha, pontos_matriz)
            if qualidade_vizinha > melhor_qualidade:
                melhor_solucao = vizinha
                melhor_qualidade = qualidade_vizinha
        if melhor_solucao is None:
            break
        solucao_atual = melhor_solucao
    return solucao_atual

def atualizarSolucao(solucao, melhorSolucao, pontos_matriz):
    if melhorSolucao is None:
        return solucao
    return solucao if calcularQualidade(solucao, pontos_matriz) > calcularQualidade(melhorSolucao, pontos_matriz) else melhorSolucao

def GRASP(maxInteracoes, LRC, pontos_matriz):
    melhorSolucao = None
    for _ in range(maxInteracoes):
        solucao = construcaoGulosaRandomica(LRC)
        solucao = buscaLocal(solucao, pontos_matriz)
        melhorSolucao = atualizarSolucao(solucao, melhorSolucao, pontos_matriz)
    return melhorSolucao

def main():
    arquivo = 'Caixeiro-Viajante/berlin52.tsp'
    pontos_matriz = lerCoordenadas(arquivo)
    LRC = list(pontos_matriz.keys())
    maxInteracoes = 100  
    melhorSolucao = GRASP(maxInteracoes, LRC, pontos_matriz)
    if melhorSolucao:
        distancia_total = -calcularQualidade(melhorSolucao, pontos_matriz)
        print(f"\nMelhor Solucao:\n {melhorSolucao} \nDistância Total: {distancia_total}")
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
