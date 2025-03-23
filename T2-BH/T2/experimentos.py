from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt


class experimento:
    """
    Classe para realizar experimentos e calcular estatísticas sobre os resultados.
    Atributos:
    ----------
    resultados : dict
        Dicionário contendo os resultados dos experimentos.
    media : float
        Média dos resultados.
    maximo : float
        Valor máximo dos resultados.
    minimo : float
        Valor mínimo dos resultados.
    std : float
        Desvio padrão dos resultados.
    estatisticas : dict
        Dicionário contendo as estatísticas calculadas para cada número de cálculos de função objetivo.
    Métodos:
    --------
    __init__(self, resultados):
        Inicializa a classe com os resultados fornecidos.
    calcula_estatisticas(self):
        Calcula as estatísticas (média, máximo, mínimo e desvio padrão) para os resultados fornecidos.
    plota_experimento(self, medida='media'):
        Plota os resultados do experimento com base na medida especificada (padrão é 'media').
    """
    
    def __init__(self, resultados, num_calculos_obj):
        self.resultados = resultados
        self.media = 0
        self.maximo = 0
        self.minimo = 0
        self.std = 0
        self.num_calculos_obj = num_calculos_obj
        self.estatisticas = {num: {'mm': {'media': self.media, 
                                          'maximo': self.maximo, 
                                          'minimo': self.minimo,
                                          'std': self.std},
                                   'pm': {'media': self.media, 
                                          'maximo': self.maximo, 
                                          'minimo': self.minimo,
                                          'std': self.std}} for num in self.num_calculos_obj}
    
    def calcula_estatisticas(self):
        for max_calc, inner in self.resultados.items():
            for k, v in inner.items():
                self.estatisticas[max_calc][k]['media'] = np.mean(v)
                self.estatisticas[max_calc][k]['maximo'] = np.max(v)
                self.estatisticas[max_calc][k]['minimo'] = np.min(v)
                self.estatisticas[max_calc][k]['std'] = np.std(v)
                
    def plota_experimento(self, medida='media', vizinhanca='Aleatória'):
        x = self.estatisticas.keys()
        medias_mm = []
        medias_pm = []
        for _, inner_dict in self.estatisticas.items():
            for metodo, v in inner_dict.items():
                if metodo == 'mm':
                    medias_mm.append(v[medida])
                if metodo == 'pm':
                    medias_pm.append(v[medida])

        plt.plot(x, medias_mm, '-o', label='MM')
        plt.plot(x, medias_pm, '-o', label='PM')
            
        plt.xlabel('Número de cálculos de função objetivo', fontsize=12)
        plt.ylabel('VPL', fontsize=12)
        plt.title(f'VPL médio por número de cálculos de função objetivo e vizinhança {vizinhanca}')
        plt.grid(True)
        plt.legend()
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        plt.ticklabel_format(style='plain', axis='x') 
