import math
import random

def lerMatriz(arquivo):
    with open(arquivo, 'r') as rota:
        linhas = rota.readlines()
    dimensoes_matriz = list(map(int, linhas[0].strip().split()))
    matriz = []
    pontos_matriz = {}
    for i in range(dimensoes_matriz[0]):
        linha = linhas[i + 1].strip().split()
        matriz.append(list(map(float, linha)))  
        for j in range(dimensoes_matriz[1]):
            if linha[j] != '0':
                pontos_matriz[linha[j]] = (i, j)
    return matriz, pontos_matriz

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
    i1, j1 = ponto1
    i2, j2 = ponto2
    return math.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)

def calcularQualidade(solucao, matriz, pontos_matriz):
    distancia_total = 0
    for i in range(len(solucao) - 1):
        ponto_atual = pontos_matriz[solucao[i]]
        proximo_ponto = pontos_matriz[solucao[i + 1]]
        distancia = calcularDistancia(ponto_atual, proximo_ponto)
        print(f'Distância de {solucao[i]} para {solucao[i + 1]}: {distancia}')
        distancia_total += distancia
    ponto_inicio = pontos_matriz[solucao[0]]
    ponto_fim = pontos_matriz[solucao[-1]]
    distancia_retorno = calcularDistancia(ponto_fim, ponto_inicio)
    print(f'Distância de {solucao[-1]} para {solucao[0]} (retorno): {distancia_retorno}')
    distancia_total += distancia_retorno
    print(f'Distância total da solução {solucao}: {distancia_total}')
    return -distancia_total  
  
def Vizinhaca(solucao):
    vizinhaca = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            vizinha = solucao[:]
            vizinha[i], vizinha[j] = vizinha[j], vizinha[i]
            vizinhaca.append(vizinha)
    return vizinhaca

def buscaLocal(solucao, matriz, pontos_matriz):
    solucao_atual = solucao
    while True:
        melhor_solucao = None
        melhor_qualidade = calcularQualidade(solucao_atual, matriz, pontos_matriz)
        vizinhaca = Vizinhaca(solucao_atual)
        for vizinha in vizinhaca:
            qualidade_vizinha = calcularQualidade(vizinha, matriz, pontos_matriz)
            if qualidade_vizinha > melhor_qualidade:
                melhor_solucao = vizinha
                melhor_qualidade = qualidade_vizinha
        if melhor_solucao is None:
            break
        solucao_atual = melhor_solucao
    return solucao_atual

def atualizarSolucao(solucao, melhorSolucao, matriz, pontos_matriz):
    if melhorSolucao is None:
        return solucao
    return solucao if calcularQualidade(solucao, matriz, pontos_matriz) > calcularQualidade(melhorSolucao, matriz, pontos_matriz) else melhorSolucao

def GRASP(maxInteracoes, LRC, matriz, pontos_matriz):
    melhorSolucao = None
    for _ in range(maxInteracoes):
        solucao = construcaoGulosaRandomica(LRC)
        vizinhaca = Vizinhaca(solucao)
        solucao = buscaLocal(solucao, matriz, pontos_matriz)
        melhorSolucao = atualizarSolucao(solucao, melhorSolucao, matriz, pontos_matriz)
    return melhorSolucao

def main():
    arquivo = 'Caixeiro-Viajante/teste.txt'
    matriz, pontos_matriz = lerMatriz(arquivo)
    for ponto, coordenadas in pontos_matriz.items():
        print(f"Pontos: \nPonto: {ponto}, Coordenadas: {coordenadas}")
    LRC = list(pontos_matriz.keys())
    maxInteracoes = 1
    melhorSolucao = GRASP(maxInteracoes, LRC, matriz, pontos_matriz)
    if melhorSolucao:
        distancia_total = -calcularQualidade(melhorSolucao, matriz, pontos_matriz)  
        print(f"\nMelhor Solucao:\n {melhorSolucao} \nDistância Total: {distancia_total}")
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
