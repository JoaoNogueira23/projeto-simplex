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
        self.c_t = None
        self.p_t = None
    
        if n > m:
            raise ValueError("Problema Ilimitado")

        # matriz base e matriz N iniciais
        self.index_base = [i for i in range(len(b))]
        self.index_n = [i for i in range(len(b), m - n)]
        self.base_matrix = A[:, self.index_base]
        self.n_matrix = A[:, self.index_n]

    def basic_solver(self):
        # calculo da inversa de B e x
        base_inverse = np.linalg.inv(self.base_matrix)

        x_basic = base_inverse @ self.indep_terms

        # calculo do vetor multiplicados
        self.c_t = self.indep_terms[:, self.index_base]
        self.p_t = self.c_t @ base_inverse

        pass
        
    