import numpy as np

class SimplexSolver:
    """
    inputs:
        m: numero de linhas (quantidade de equações)
        n: numero de colunas (quantidade de variáveis)
        c: vetor dos custos (vetor com os coeficientes da função minimizadora)
        b: vetor de recursos (termo independente)
        a: matriz dos coeficientes das restrições
    """
    def __init__(self, m:int, n:int, c: np.array, b: np.array, A: np.array):
        self.lines = m
        self.columns = n
        self.cost_matrix = c
        self.indep_terms = b
        self.coefs_matrix = A
    
        if n > m:
            raise ValueError("Problema Ilimitado")
        
    