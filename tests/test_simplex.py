import numpy as np
from SimplexMethod import SimplexSolver


def test_example_problem():
    # Problema do README / exemplo no final de SimplexMethod.py
    A = np.array([[1, 1, 1, 0],
                  [1, 3, 0, 1]], dtype=float)
    b = np.array([4, 6], dtype=float)
    c = np.array([3, 2, 0, 0], dtype=float)
    m, n = A.shape

    # base inicial: colunas 2 e 3 (variáveis de folga s1, s2)
    base = [2, 3]
    solver = SimplexSolver(m, n, c, b, A, index_base=base)
    result = solver.solve()

    # A solução ótima conhecida para esse problema tem x = [0, 2, 2, 0]
    # com custo objetivo 3*0 + 2*2 = 4
    assert result["status"] == "ótima"
    # checar objetivo dentro de tolerância
    assert abs(result["objetivo"] - 4.0) < 1e-8
    x = result["x"]
    assert x.shape == (n,)
    # verificar componentes esperados aproximados
    assert abs(x[0] - 0.0) < 1e-8
    assert abs(x[1] - 2.0) < 1e-8
    assert abs(x[2] - 2.0) < 1e-8
    assert abs(x[3] - 0.0) < 1e-8
