"""Independent real-MPS verifier. No TeNPy imports, MPOs, or optimizer energies.

Every binary64 tensor entry is an exact dyadic rational. Integer transfer
contractions compute the Rayleigh quotient EXACTLY, including normalization.
The witness denotes the tensor product contraction divided by its exact norm.
"""
from fractions import Fraction
from functools import reduce
from math import lcm
from pathlib import Path
import hashlib
import json
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
I = np.eye(2, dtype=int)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1], [1, 0]])  # i*sigma_y; sigma_y sigma_y = -Y Y
Z = np.diag([-1, 1])             # basis [down, up]
OPS = (X, Y, Z)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def suite():
    return json.loads((ROOT / 'benchmarks/suite.json').read_text())


def case_by_id(name):
    return next(c for c in suite()['instances'] if c['id'] == name)


def hamiltonian_id(case):
    physical = {k: case[k] for k in ('L', 'J1', 'J2', 'delta', 'boundary', 'basis')}
    return hashlib.sha256(json.dumps(physical, sort_keys=True).encode()).hexdigest()


def validate_tensors(tensors, case):
    if len(tensors) != case['L']:
        raise ValueError('wrong length')
    left = 1
    for a in tensors:
        if a.dtype != np.dtype('float64') or a.ndim != 3:
            raise ValueError('only real binary64 (left, physical, right) tensors accepted')
        if a.shape[0] != left or a.shape[1] != 2 or not (1 <= a.shape[2] <= case['chi_max']):
            raise ValueError('invalid shape or bond limit')
        if not np.isfinite(a).all() or np.max(np.abs(a)) > 2:
            raise ValueError('nonfinite or badly scaled tensor')
        left = a.shape[2]
    if left != 1:
        raise ValueError('open boundary requires final bond one')


def load_witness(path, case):
    path = Path(path)
    if path.stat().st_size > 8_000_000:
        raise ValueError('oversized archive')
    with zipfile.ZipFile(path) as z:
        if sum(i.file_size for i in z.infolist()) > 16_000_000:
            raise ValueError('oversized expanded archive')
    with np.load(path, allow_pickle=False) as z:
        if set(z.files) != {'hamiltonian_id', *[f'A{i}' for i in range(case['L'])]}:
            raise ValueError('unexpected witness keys')
        if str(z['hamiltonian_id']) != hamiltonian_id(case):
            raise ValueError('Hamiltonian mismatch')
        tensors = [z[f'A{i}'] for i in range(case['L'])]
    validate_tensors(tensors, case)
    return tensors


def transfer(env, a, op):
    out = np.zeros((a.shape[2], a.shape[2]), dtype=a.dtype)
    for s in range(2):
        for t in range(2):
            if op[s, t]:
                out += int(op[s, t]) * (a[:, s, :].T @ env @ a[:, t, :])
    return out


def coefficients(case):
    # H = sum J/4 (XX - YY + delta ZZ), no field, no wrapping bonds.
    return [[Fraction(case[j]) * v / 4 for v in
             (Fraction(1), Fraction(-1), Fraction(case['delta']))] for j in ('J1', 'J2')]


def contraction(tensors, case, exact=True):
    coeff = coefficients(case)
    denominator = reduce(lcm, [x.denominator for row in coeff for x in row], 1)
    weights = [[int(x * denominator) for x in row] for row in coeff]
    dtype = object if exact else np.float64
    norm = np.ones((1, 1), dtype=dtype)
    energy = np.zeros((1, 1), dtype=dtype)
    previous = [np.zeros((1, 1), dtype=dtype) for _ in OPS]
    previous2 = [np.zeros((1, 1), dtype=dtype) for _ in OPS]
    scale = 0
    for a0 in tensors:
        if exact:
            ratios = [float(x).as_integer_ratio() for x in a0.flat]
            shift = max(d.bit_length() - 1 for _, d in ratios)
            a = np.array([n << (shift - (d.bit_length() - 1)) for n, d in ratios],
                         dtype=object).reshape(a0.shape)
            scale += 2 * shift
        else:
            a = a0
        updated = transfer(energy, a, I)
        for k, op in enumerate(OPS):
            updated += weights[0][k] * transfer(previous[k], a, op)
            updated += weights[1][k] * transfer(previous2[k], a, op)
        previous2 = [transfer(p, a, I) for p in previous]
        previous = [transfer(norm, a, op) for op in OPS]
        norm = transfer(norm, a, I)
        energy = updated
    if exact:
        n = int(norm[0, 0])
        if n <= 0:
            raise ValueError('zero state')
        return Fraction(int(energy[0, 0]), denominator * n), Fraction(n, 1 << scale)
    return float(energy[0, 0] / (denominator * norm[0, 0])), float(norm[0, 0])


def decimal_interval(value, digits=14):
    """Outward decimal enclosure using only integer arithmetic."""
    scale = 10 ** digits
    lower = value.numerator * scale // value.denominator
    upper = -((-value.numerator * scale) // value.denominator)
    def fmt(n):
        return ('-' if n < 0 else '') + str(abs(n) // scale) + '.' + str(abs(n) % scale).zfill(digits)
    return [fmt(lower), fmt(upper)]


def verify(path, case, claim=None):
    tensors = load_witness(path, case)
    e, n = contraction(tensors, case)
    if abs(n - 1) > Fraction(1, 10**8):
        raise ValueError('raw norm outside 1e-8; normalized representation required')
    if claim is not None:
        # Claimed printed energy is checked to fixed precision, never author-selected tolerance.
        q = Fraction(str(claim))
        if abs(q - e) > Fraction(1, 10**10):
            raise ValueError('false energy claim')
    return {'energy': float(e), 'energy_interval': decimal_interval(e),
            'norm_interval': decimal_interval(n), 'witness_sha256': digest(path),
            'hamiltonian_id': hamiltonian_id(case),
            'max_bond': max(a.shape[2] for a in tensors),
            'certificate': 'exact dyadic integer contraction; outward decimal Rayleigh quotient enclosure'}


def dense_state(tensors):
    state = np.ones((1, 1))
    for a in tensors:
        state = np.einsum('xa,asb->xsb', state, a).reshape(-1, a.shape[2])
    return state[:, 0]
