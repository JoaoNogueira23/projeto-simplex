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
        self.matriz_custos_relativos = None
        self.x_basico = None
        self.base_inverse = None
    
        if n > m:
            raise ValueError("Problema Ilimitado")

        # matriz base e matriz N iniciais
        self.index_base = [i for i in range(len(b))]
        self.index_n = [i for i in range(len(b), m - n)]
        self.base_matrix = A[:, self.index_base]
        self.n_matrix = A[:, self.index_n]

    def solucao_basica(self):
        # calculo da inversa de B e x
        base_inverse = np.linalg.inv(self.base_matrix)
        self.base_inverse = base_inverse

        x_basic = base_inverse @ self.indep_terms
        self.x_basico = x_basic

        # calculo do vetor multiplicados
        self.c_t = self.indep_terms[:, self.index_base]
        self.p_t = self.c_t @ base_inverse

        #calculo dos custos relativos
        matriz_custos_relativos = self.cost_matrix - self.coefs_matrix
        self.matriz_custos_relativos = matriz_custos_relativos
        if np.nonzero(matriz_custos_relativos)[0].size != 0:
            print("Solução ótima ainda não encontrada")
    
    def teste_razao(self):
        min_global = self.matriz_custos_relativos.argmin()
        coordenadas = np.unravel_index(min_global, self.coefs_matrix)
        column_indice = coordenadas[1]

        ref_column_to_calculate = self.indep_terms[:, column_indice]
        base_inverse = self.base_inverse
        if self.base_inverse:
            base_inverse = np.linalg.inv(self.base_matrix)
        
        y_calculate = base_inverse @ ref_column_to_calculate
        indice_min_global = y_calculate.argmin()
        
        pass

        
    