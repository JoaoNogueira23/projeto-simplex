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
        self.degress_freedom = m - n # quantidade de colunas na matriz N
        self.base_matrix = None
        self.n_matrix = None
    
        if n > m:
            raise ValueError("Problema Ilimitado")

        self.index_base = [i for i in range(len(b))]
        self.index_n = [i for i in range(m-n)]

    def basic_solver(self):
        # calculo da inversa de B
        
        pass
        
    