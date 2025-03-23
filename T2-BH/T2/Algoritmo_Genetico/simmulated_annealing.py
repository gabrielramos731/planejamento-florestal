import random
import math
import time
import numpy as np
import pandas as pd
import sys
import os
# import importlib
import matplotlib.pyplot as plt

# Adiciona o diretório anterior ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import aux_func  # Agora você pode importar aux_func
# importlib.reload(aux_func)

def gera_vizinhos(df, vet_solucao):
    """
    Gera vizinhos de um talhão sorteado
    """
    talhao_sorteado = random.randint(0, 119)
    prescricao_sorteada = np.random.choice(df[df['talhao'] == talhao_sorteado+1]['prescrição'].unique()) # sorteia prescrição

    vizinho = vet_solucao.copy()
    vizinho[talhao_sorteado] = prescricao_sorteada # altera solução
    return vizinho

def gera_vizinhos_localizado(df, solucao):
    """
    Gera uma lista de vizinhos localizados para uma solução dada.
    Esta função identifica o pior ano em uma solução e, em seguida, encontra
    todos os talhões que podem ser colhidos naquele ano com base nas idades
    de colheita fornecidas.
    Args:
        df (pd.DataFrame): DataFrame contendo informações sobre os talhões,
                             incluindo a idade de cada talhão.
        solucao (list): Lista representando a solução atual.
        idade_colheita (dict): Dicionário onde as chaves são anos e os valores
                               são listas de idades possíveis para colheita
                               naquele ano.
    Returns:
        None: A função imprime o pior ano e os talhões possíveis para colheita
              naquele ano.
    """
    
    idade_colheita = {1: ['5', '6'],
                  2: ['4', '5', '6'],
				  3: ['3', '4', '5'],
				  4: ['2', '3', '4'],
				  5: ['1', '2', '3'],
				  6: ['1', '2', '5', '6'],
				  7: ['1', '4', '5', '6'],
				  8: ['3', '4', '5', '6'],
				  9: ['2', '3', '4', '5', '6'],
				  10: ['1', '2', '3', '4', '5'],
				  11: ['1', '2', '3', '4', '5', '6'],
				  12: ['1', '2', '3', '4', '5', '6'],
				  13: ['1', '2', '3', '4', '5', '6'],
				  14: ['1', '2', '3', '4', '5', '6'],
				  15: ['1', '2', '3', '4', '5', '6'],
				  16: ['1', '2', '3', '4', '5', '6']}
    pior_ano = aux_func.encontra_pior_ano(df, solucao)
    possiveis_idades = idade_colheita[pior_ano]
    possiveis_talhoes = df[np.isin(df.loc[:, 'idade'], list(map(int, possiveis_idades)))]['talhao'].unique() # talhoes que podem fazer colheita naquele ano
    talhao_sorteado = random.sample(list(possiveis_talhoes), 1) # talhão sorteado
    prescricao_talhao = np.random.choice(df[df['talhao'] == talhao_sorteado[0]]['prescrição'].unique()) # prescrição sorteada
    vizinho = solucao.copy()
    vizinho[talhao_sorteado[0]-1] = prescricao_talhao # altera solução

    return vizinho


def simulated_annealing(df, sol_atual, **kwargs):
    time_ini = time.time()
    temperatura = kwargs.get('temp_inicial', 1000)
    final_temp = kwargs.get('final_temp', 1)
    cooling_rate = kwargs.get('cooling_rate', 0.9)
    vizinhanca = kwargs.get('vizinhanca', 'aleatoria')
    max_calculos_obj = kwargs.get('max_calculos_obj', 10000)
    max_iter = kwargs.get('max_iter', 100)
    random.seed(kwargs.get('seed', 42))

    counter_calculos_obj, count_aceitou, count_nao_aceitou = 0, 0, 0
    melhor_solucao_global = sol_atual
    melhor_vpl_global = aux_func.calcula_vpl_total(df, sol_atual)

    vpl_teste = []
    
    while temperatura > final_temp:
        if temperatura < 1e-6:
            break
        if counter_calculos_obj >= max_calculos_obj:
            print("Número máximo de cálculos atingido")
            break
        for _ in range(max_iter): # número de iterações por temperatura
            if counter_calculos_obj >= max_calculos_obj:
                break
            
            # Geração de vizinhos
            if vizinhanca == 'aleatoria':
                novo_vizinho = gera_vizinhos(df, sol_atual)
            elif vizinhanca == 'localizada':
                novo_vizinho = gera_vizinhos_localizado(df, sol_atual)

            vpl_novo_vizinho = aux_func.calcula_vpl_total(df, novo_vizinho)
            vpl_atual = aux_func.calcula_vpl_total(df, sol_atual)
            counter_calculos_obj += 2

            rand = random.random()
            prob = math.exp(-(vpl_atual - vpl_novo_vizinho) / temperatura)
            
            # Aceitação da solução
            if vpl_novo_vizinho > vpl_atual or rand < prob:
                sol_atual = novo_vizinho
                if vpl_novo_vizinho > melhor_vpl_global:
                    melhor_vpl_global = vpl_novo_vizinho
                    melhor_solucao_global = novo_vizinho
                count_aceitou += 1
            else:
                count_nao_aceitou += 1
                
            vpl_teste.append(vpl_atual)            
        temperatura *= cooling_rate
    
    time_exec = time.time() - time_ini
    print(f'Tempo de execução: {time_exec:.2f} s')
    print(f'Temperatura: {temperatura:.2f} | Aceitou: {count_aceitou} | Não aceitou: {count_nao_aceitou}')
    return melhor_vpl_global, melhor_solucao_global, vpl_teste

