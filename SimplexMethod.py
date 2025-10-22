import numpy as np

class SimplexSolver:
    """
    Simplex primal (minimização) para problemas na forma:
        minimize    c^T x
        subject to  A x = b
                    x >= 0

    Requer uma base inicial (index_base) de tamanho m (números de equações).
    Se não fornecer index_base, o solver tentará encontrar colunas que formem
    uma matriz identidade (slack variables típicas).

    Parâmetros:
        m (int): número de equações (linhas)
        n (int): número de variáveis totais (colunas em A)
        c (np.array): vetor de custos (shape (n,))
        b (np.array): vetor independentes (shape (m,))
        A (np.array): matriz de coeficientes (shape (m, n))
        index_base (list[int], opcional): índices das colunas básicas iniciais (len = m)
    """
    def __init__(self, m:int, n:int, c: np.ndarray, b: np.ndarray, A: np.ndarray, index_base=None):
        self.m = m
        self.n = n
        self.c = np.asarray(c).astype(float).reshape(-1)
        self.b = np.asarray(b).astype(float).reshape(-1)
        self.A = np.asarray(A).astype(float)
        assert self.A.shape == (m, n)
        assert self.c.shape[0] == n
        assert self.b.shape[0] == m

        # base inicial: se não vier, tenta achar colunas identidade
        if index_base is None:
            index_base = self._find_identity_base()
        if index_base is None:
            raise ValueError("Nenhuma base inicial encontrada automaticamente. Forneça index_base ou rode Fase I.")
        if len(index_base) != m:
            raise ValueError("index_base deve ter comprimento m (número de equações).")

        self.index_base = list(index_base)
        self.index_nonbase = [j for j in range(n) if j not in self.index_base]

        # estado
        self.B_inv = None
        self.x = np.zeros(n)
        self.iterations = 0
        self.max_iterations = 1000

    def _find_identity_base(self):
        """Tenta encontrar colunas de A que formem a identidade para otimizar o calculo
        """
        m, n = self.A.shape
        identity_cols = []
        for j in range(n):
            col = self.A[:, j]
            # coluna é uma coluna base candidata se tem exatamente um 1 e resto 0
            if np.count_nonzero(col == 0.0) == m - 1 and np.count_nonzero(col == 1.0) == 1:
                # posição do 1 deverá ser única
                one_pos = np.where(col == 1.0)[0][0]
                # garantir que essa posição ainda livre
                if one_pos not in [np.where(self.A[:, k] == 1.0)[0][0] if np.count_nonzero(self.A[:, k] == 1.0) == 1 and np.count_nonzero(self.A[:, k] == 0.0) == m - 1 else None for k in identity_cols]:
                    identity_cols.append(j)
            if len(identity_cols) == m:
                break
        if len(identity_cols) == m:
            return identity_cols
        return None

    def _compute_basic_solution(self):
        """Calcula B_inv, x_B e atualiza x (com zeros para não-básicas)."""
        B = self.A[:, self.index_base] #matriz base
        try:
            B_inv = np.linalg.inv(B) # inversa da matriz base
        except np.linalg.LinAlgError:
            raise ValueError("Matriz base singular — base inválida.")
        self.B_inv = B_inv
        x_B = B_inv @ self.b

        # montar solução basica
        x = np.zeros(self.n)
        for i, idx in enumerate(self.index_base):
            x[idx] = x_B[i]
        self.x = x
        return x_B

    def _reduced_costs(self):
        """Calcula os custos relativos r = c - c_B^T B^{-1} A"""
        c_B = np.array([self.c[j] for j in self.index_base])
        # pi^T = c_B^T B^{-1}
        piT = c_B @ self.B_inv

        reduced = self.c - (piT @ self.A)
        return reduced, piT

    def _ratio_test(self, column_idx):
        """Faz teste razão para coluna de direção (entrante)."""
        a_j = self.A[:, column_idx]
        d = self.B_inv @ a_j  # direção nas variáveis básicas
        x_B = np.array([self.x[idx] for idx in self.index_base])
        # razão somente para d > 0
        positive = d > 1e-12
        if not np.any(positive):
            return None, d  # ilimitado
        ratios = np.full_like(d, np.inf, dtype=float)
        ratios[positive] = x_B[positive] / d[positive]
        # menor razão, escolher menor índice em caso de empate (Bland-like tie-break)
        leave_pos = int(np.argmin(ratios))
        min_ratio = ratios[leave_pos]
        return leave_pos, d

    def _pivot(self, entering_idx, leaving_pos):
        """Faz troca de base: substitui index_base[leaving_pos] por entering_idx."""
        leaving_var = self.index_base[leaving_pos]
        # atualizar índices de base
        self.index_base[leaving_pos] = entering_idx
        # recomputar conjunto não-base
        self.index_nonbase = [j for j in range(self.n) if j not in self.index_base]
        # recomputar B_inv e x
        self._compute_basic_solution()

    def solve(self, max_iter=500):
        """Executa o simplex primal até otimidade ou ilimitado. Retorna solução e custo."""
        self.max_iterations = max_iter
        _ = self._compute_basic_solution()
        self.iterations = 0

        while self.iterations < self.max_iterations:
            self.iterations += 1
            reduced, piT = self._reduced_costs()
            # escolha variável entrante: custo relativo negativo mais negativo (minimização)
            # se todos >= 0, solução ótima encontrada (para)
            entering_candidates = np.where(reduced < -1e-9)[0]
            if entering_candidates.size == 0:
                # ótimo
                objective = float(self.c @ self.x)
                return {"status": "ótima", "x": self.x, "objetivo": objective, "iterações": self.iterations}
            # escolha pelo menor custo reduzido (mais negativo); tie-break pelo menor índice (Bland)
            entering_idx = int(entering_candidates[np.argmin(reduced[entering_candidates])])

            # teste razão (para escolher quem vai entrar na base para a nova interação)
            leaving_pos, d = self._ratio_test(entering_idx)
            if leaving_pos is None:
                # direção não positiva -> ilimitado
                return {"status": "ilimitada", "input": entering_idx, "d": d}
            # faz a troca de base apos definido quem vai entrar
            self._pivot(entering_idx, leaving_pos)

        return {"status": "interações máximas excedidadas", "iterações": self.iterations}

# ---------------------------
# Exemplo de uso:
# Minimize 3 x1 + 2 x2
# subject to:
#    x1 + x2 <= 4
#    x1 + 3 x2 <= 6
# x >= 0
#
# adicionamos slacks s1, s2 => variáveis [x1, x2, s1, s2]
# A = [[1, 1, 1, 0],
#      [1, 3, 0, 1]]
# b = [4, 6]
# c = [3, 2, 0, 0]
if __name__ == "__main__":
    A = np.array([[1, 1, 1, 0],
                  [1, 3, 0, 1]], dtype=float)
    b = np.array([4, 6], dtype=float)
    c = np.array([3, 2, 0, 0], dtype=float)
    m, n = A.shape
    # base inicial composta pelas colunas 2 e 3 (s1 e s2)
    base = [2, 3]
    solver = SimplexSolver(m, n, c, b, A, index_base=base)
    result = solver.solve()
    print(result)
