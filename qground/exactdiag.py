"""Independent bit-basis Hamiltonian; never uses optimizer or transfer code."""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh


def matrix(case):
    L = case['L']
    if L > 16:
        raise ValueError('ED limited to 16 sites')
    states = np.arange(1 << L, dtype=np.int64)
    diagonal = np.zeros(len(states))
    rows, cols, values = [], [], []
    for distance, j in ((1, float(case['J1'])), (2, float(case['J2']))):
        for i in range(L - distance):
            a, b = 1 << (L-1-i), 1 << (L-1-i-distance)
            unequal = ((states & a) != 0) != ((states & b) != 0)
            diagonal += np.where(unequal, -1, 1) * j * float(case['delta']) / 4
            selected = states[unequal]
            rows.extend(selected.tolist())
            cols.extend((selected ^ a ^ b).tolist())
            values.extend([j / 2] * len(selected))
    rows.extend(states.tolist()); cols.extend(states.tolist()); values.extend(diagonal.tolist())
    return coo_matrix((values, (rows, cols)), shape=(len(states), len(states))).tocsr()


def reference(case):
    h = matrix(case)
    if case['L'] <= 8:
        eigenvalues, vectors = np.linalg.eigh(h.toarray())
        e, v = eigenvalues[0], vectors[:, 0]
    else:
        rng = np.random.default_rng(91073 + case['L'])
        eigenvalues, vectors = eigsh(h, k=2, which='SA', tol=1e-12,
                                     v0=rng.normal(size=h.shape[0]), maxiter=20000)
        index = np.argmin(eigenvalues)
        e, v = eigenvalues[index], vectors[:, index]
    r = np.linalg.norm(h @ v - e * v)
    return {'energy': float(e), 'residual_norm': float(r),
            'status': 'numerical full-Hilbert-space ED reference, not certified global lower bound'}
