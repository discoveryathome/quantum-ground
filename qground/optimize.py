"""TeNPy proposal generator. Verifier is a separate module with no TeNPy import."""
import time
import copy
import numpy as np
import tenpy
from tenpy.models.spins_nnn import SpinChainNNN2
from tenpy.networks.mps import MPS
from tenpy.algorithms.dmrg import TwoSiteDMRGEngine, SingleSiteDMRGEngine
from .evaluator import hamiltonian_id

METHODS = ['baseline', 'ramp', 'dimer', 'random', 'single_site']


def model(case):
    j1, j2, delta = map(float, (case['J1'], case['J2'], case['delta']))
    return SpinChainNNN2({'L': case['L'], 'S': 0.5, 'conserve': None,
        'bc_MPS': 'finite', 'bc_x': 'open', 'Jx': j1, 'Jy': j1, 'Jz': j1*delta,
        'Jxp': j2, 'Jyp': j2, 'Jzp': j2*delta, 'hx': 0., 'hy': 0., 'hz': 0.})


def arrays(psi):
    # Contract B-form tensors: leftmost Schmidt value and global norm are one.
    result = []
    for i in range(psi.L):
        a = psi.get_B(i, form='B').transpose(['vL', 'p', 'vR']).to_ndarray()
        if np.iscomplexobj(a) and np.max(abs(a.imag)) > 1e-13:
            raise ValueError('complex candidate outside real pilot')
        result.append(np.asarray(a.real, dtype=np.float64))
    return result


def save(path, tensors, case):
    np.savez_compressed(path, hamiltonian_id=hamiltonian_id(case),
                        **{f'A{i}': a for i, a in enumerate(tensors)})


def run(case, method, seed, directory, sweeps=6):
    start_cpu, start_wall = time.process_time(), time.perf_counter()
    m = model(case)
    sites = m.lat.mps_sites()
    if method == 'dimer':
        psi = MPS.from_singlets(sites[0], case['L'], [(i,i+1) for i in range(0,case['L'],2)])
    elif method == 'random':
        rng = np.random.default_rng(seed)
        angles = rng.uniform(0, 2*np.pi, case['L'])
        psi = MPS.from_product_state(sites, [[np.cos(a), np.sin(a)] for a in angles], bc='finite')
    else:
        psi = MPS.from_product_state(sites, ['up','down']*(case['L']//2), bc='finite')
    options = {'trunc_params': {'chi_max': case['chi_max'], 'svd_min': 1e-14, 'trunc_cut': None},
               'mixer': True, 'mixer_params': {'amplitude': 1e-5, 'decay': 10., 'disable_after': 3},
               'diag_method': 'lanczos', 'lanczos_params': {'N_max': 40, 'N_min': 2, 'P_tol': 1e-12, 'E_tol': 1e-12},
               'combine': True}
    if method == 'ramp':
        options['chi_list'] = {0: 2, 1: 4, 2: case['chi_max']}
    engine_cls = SingleSiteDMRGEngine if method == 'single_site' else TwoSiteDMRGEngine
    input_options = copy.deepcopy(options)
    engine = engine_cls(psi, m, options)
    engine.pre_run_initialize()
    history = []
    # Time includes model/initialization and optimizer; excludes checkpoint I/O and scoring.
    excluded_cpu = excluded_wall = 0.
    for sweep in range(sweeps):
        engine.sweep()
        if sweep == sweeps - 1 and engine.mixer is not None:
            engine.mixer_deactivate()
        engine.mixer_cleanup()
        elapsed_cpu = time.process_time() - start_cpu - excluded_cpu
        elapsed_wall = time.perf_counter() - start_wall - excluded_wall
        t_cpu, t_wall = time.process_time(), time.perf_counter()
        tensors = arrays(psi)
        path = directory / f'sweep-{sweep+1}.npz'
        save(path, tensors, case)
        history.append({'sweep': sweep+1, 'cpu_seconds': elapsed_cpu, 'wall_seconds': elapsed_wall,
                        'optimizer_energy': float(m.H_MPO.expectation_value(psi)),
                        'witness': str(path), 'max_bond': int(max(psi.chi))})
        excluded_cpu += time.process_time() - t_cpu
        excluded_wall += time.perf_counter() - t_wall
    return {'method': method, 'instance': case['id'], 'seed': seed, 'history': history,
            'cpu_seconds': history[-1]['cpu_seconds'], 'wall_seconds': history[-1]['wall_seconds'],
            'tenpy_version': tenpy.__version__, 'options': input_options,
            'local_updates': len(engine.update_stats['i0']),
            'lanczos_iterations': int(sum(engine.update_stats['N_lanczos']))}
